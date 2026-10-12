from __future__ import annotations

import json
import math
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import os
from threading import Lock
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException

from src.forecasting.forecast_state import ForecastState
from src.forecasting.model_interface import ForecastModel
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_future_feature_builder import (
    RecursiveFutureFeatureBuilder,
)
from src.forecasting.ridge_model import RidgeDemandModel


ROOT = Path(__file__).resolve().parent
TRAINING_FILE = ROOT / "data" / "features" / "training_split.json"
CONFIG_FILE = ROOT / "data" / "features" / "ridge_model_config.json"

app = FastAPI(
    title="Restaurant Demand Prediction API",
    description=(
        "Accept historical demand data and return recursive "
        "demand forecasts. Additional input columns are supported."
    ),
    version="1.0.0",
)


def load_model() -> ForecastModel:
    """Train once at application startup using existing training data."""
    if not TRAINING_FILE.exists():
        raise RuntimeError(f"Training data not found: {TRAINING_FILE}")

    with TRAINING_FILE.open(encoding="utf-8") as file:
        split = json.load(file)

    config = {}
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open(encoding="utf-8") as file:
            config = json.load(file)

    model = RidgeDemandModel(
        alpha=float(config.get("alpha", 1.0))
    )
    model.fit(split["train"])
    return model


# A single fitted model is reused across API requests.
MODEL = load_model()
FEATURE_BUILDER = RecursiveFutureFeatureBuilder()


def make_predictor(features: Any) -> float:
    """Adapt the existing feature builder's output to Ridge."""
    row = asdict(features)
    return MODEL.predict([row])[0]


PREDICTION_ADAPTER = PredictionAdapter(make_predictor)



# TEMPORARY DATA COLLECTION — migrate to PostgreSQL next.
DATA_DIR = ROOT / "data" / "collected"
SALES_FILE = DATA_DIR / "sales.jsonl"
DATA_LOCK = Lock()

DATA_FIELDS = {
    "restaurant_id",
    "date",
    "item_id",
    "units_sold",
}

OPTIONAL_FIELDS = {
    "item_name",
    "is_open",
    "stockout_flag",
    "promotion_flag",
    "opening_stock",
    "received_stock",
    "waste_units",
    "closing_stock",
    "unit_price",
    "weather",
    "data_source",
}


def read_sales_records() -> list[dict[str, Any]]:
    """Read all collected records from the JSONL file."""
    if not SALES_FILE.exists():
        return []

    records = []
    with SALES_FILE.open(encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))
    return records


@app.post("/data/ingest")
def ingest_sales(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Save daily sales records.

    Example:
    {
      "records": [
        {
          "restaurant_id": 1,
          "date": "2026-10-12",
          "item_id": 101,
          "units_sold": 18
        }
      ]
    }
    """
    rows = payload.get("records")

    if not isinstance(rows, list) or not rows:
        raise HTTPException(
            status_code=422,
            detail="'records' must be a non-empty list",
        )

    if len(rows) > 5000:
        raise HTTPException(
            status_code=413,
            detail="Maximum 5000 records per request",
        )

    prepared = []
    seen = set()

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise HTTPException(
                status_code=422,
                detail=f"Record {index} must be an object",
            )

        missing = DATA_FIELDS - row.keys()
        if missing:
            raise HTTPException(
                status_code=422,
                detail=f"Record {index} missing fields: {sorted(missing)}",
            )

        try:
            restaurant_id = int(row["restaurant_id"])
            item_id = int(row["item_id"])
            units_sold = float(row["units_sold"])
            record_date = date.fromisoformat(str(row["date"]))
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid values in record {index}",
            ) from exc

        if restaurant_id <= 0 or item_id <= 0:
            raise HTTPException(
                status_code=422,
                detail=f"Record {index}: IDs must be positive",
            )

        if not math.isfinite(units_sold) or units_sold < 0:
            raise HTTPException(
                status_code=422,
                detail=f"Record {index}: units_sold must be non-negative",
            )

        if not units_sold.is_integer():
            raise HTTPException(
                status_code=422,
                detail=f"Record {index}: units_sold must be a whole number",
            )

        key = (restaurant_id, record_date.isoformat(), item_id)

        if key in seen:
            raise HTTPException(
                status_code=422,
                detail=f"Duplicate item/date in request: {key}",
            )
        seen.add(key)

        clean = {
            "restaurant_id": restaurant_id,
            "date": record_date.isoformat(),
            "item_id": item_id,
            "units_sold": int(units_sold),
        }

        for field in OPTIONAL_FIELDS:
            if field in row:
                clean[field] = row[field]

        prepared.append((key, clean))

    with DATA_LOCK:
        try:
            existing = read_sales_records()
        except (OSError, json.JSONDecodeError) as exc:
            raise HTTPException(
                status_code=500,
                detail="Could not read the existing sales file",
            ) from exc

        existing_keys = {
            (
                int(r["restaurant_id"]),
                str(r["date"]),
                int(r["item_id"]),
            )
            for r in existing
        }

        duplicates = [
            key for key, _ in prepared if key in existing_keys
        ]

        if duplicates:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Some restaurant/item/date records already exist. "
                    "No records were saved. Correct or review the duplicates."
                ),
            )

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)

            with SALES_FILE.open("a", encoding="utf-8") as file:
                for _, record in prepared:
                    file.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )
        except OSError as exc:
            raise HTTPException(
                status_code=500,
                detail="Could not save sales records",
            ) from exc

    return {
        "status": "success",
        "records_saved": len(prepared),
        "file": "data/collected/sales.jsonl",
    }


@app.get("/data/summary")
def sales_summary() -> dict[str, Any]:
    """Summarize the collected records."""
    try:
        records = read_sales_records()
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not read collected data",
        ) from exc

    restaurants = {r["restaurant_id"] for r in records}
    items = {
        (r["restaurant_id"], r["item_id"]) for r in records
    }
    dates = {r["date"] for r in records}

    return {
        "total_records": len(records),
        "restaurant_count": len(restaurants),
        "restaurant_item_pairs": len(items),
        "dates_collected": sorted(dates),
        "storage": "temporary JSONL",
    }


@app.get("/data/export")
def export_sales() -> JSONResponse:
    """Export collected records as a JSON array."""
    try:
        records = read_sales_records()
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not read collected data",
        ) from exc

    return JSONResponse(
        content={"records": records},
        headers={
            "Content-Disposition":
                'attachment; filename="restaurant_sales.json"'
        },
    )



@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Restaurant Demand Prediction API",
        "status": "running",
        "docs": "/docs",
        "prediction_endpoint": "POST /predict",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "model": MODEL.name,
        "model_fitted": MODEL.fitted,
    }


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Required JSON:
      restaurant, item_id, start_date, horizon, history

    history is a list of records containing date and demand_quantity.
    Optional column_mapping maps canonical field names to incoming names.
    Extra fields in each record are ignored.
    """
    try:
        restaurant = int(payload["restaurant"])
        item_id = int(payload["item_id"])
        start_date = date.fromisoformat(str(payload["start_date"]))
        horizon = int(payload["horizon"])
        history_rows = payload["history"]
        column_mapping = payload.get("column_mapping", {})

        if restaurant <= 0 or item_id <= 0:
            raise ValueError("restaurant and item_id must be positive integers")

        if not 1 <= horizon <= 60:
            raise ValueError("horizon must be between 1 and 60 days")

        if not isinstance(history_rows, list) or not history_rows:
            raise ValueError("history must be a non-empty list of records")

        if not isinstance(column_mapping, dict):
            raise ValueError("column_mapping must be a JSON object")

        date_column = column_mapping.get("date", "date")
        demand_column = column_mapping.get(
            "demand_quantity", "demand_quantity"
        )

        # Aggregate transactions into daily demand. Extra columns are ignored.
        demand_history: dict[date, float] = {}

        for index, row in enumerate(history_rows):
            if not isinstance(row, dict):
                raise ValueError(f"history row {index} must be an object")

            if date_column not in row or demand_column not in row:
                raise ValueError(
                    f"history row {index} must contain "
                    f"'{date_column}' and '{demand_column}'"
                )

            historical_date = date.fromisoformat(str(row[date_column]))
            quantity = float(row[demand_column])

            if not math.isfinite(quantity) or quantity < 0:
                raise ValueError(
                    f"Invalid demand quantity in history row {index}"
                )

            demand_history[historical_date] = (
                demand_history.get(historical_date, 0.0) + quantity
            )

        required_dates = [
            start_date - timedelta(days=offset)
            for offset in range(1, 29)
        ]
        missing_dates = [
            day.isoformat()
            for day in required_dates
            if day not in demand_history
        ]

        if missing_dates:
            raise ValueError(
                "Missing historical demand for required dates: "
                + ", ".join(missing_dates[:10])
                + (
                    f" (and {len(missing_dates) - 10} more)"
                    if len(missing_dates) > 10 else ""
                )
            )

        state = ForecastState(demand=demand_history)
        predictions = []

        # Use the existing feature builders and prediction adapter.
        for offset in range(horizon):
            forecast_date = start_date + timedelta(days=offset)

            features = FEATURE_BUILDER.build(
                forecast_date=forecast_date,
                restaurant=restaurant,
                item_id=item_id,
                state=state,
            )

            predicted_demand = PREDICTION_ADAPTER.predict(features)
            state.add_prediction(forecast_date, predicted_demand)

            predictions.append({
                "date": forecast_date.isoformat(),
                "predicted_demand": round(predicted_demand, 4),
            })

        return {
            "status": "success",
            "model": MODEL.name,
            "restaurant": restaurant,
            "item_id": item_id,
            "forecast_start": start_date.isoformat(),
            "horizon_days": horizon,
            "history_rows_received": len(history_rows),
            "predictions": predictions,
        }

    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc





@app.post("/predict/batch")
def predict_batch(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Forecast all menu items for one restaurant in one request.

    Required JSON:
    {
        "restaurant": 1,
        "start_date": "2026-10-13",
        "horizon": 7,
        "items": [
            {
                "item_id": 101,
                "item_name": "Butter Chicken",
                "history": [
                    {"date": "2026-09-15", "demand_quantity": 12}
                ]
            }
        ]
    }

    Each item's history must contain all 28 consecutive days
    immediately before start_date.
    """
    try:
        restaurant = int(payload["restaurant"])
        start_date = date.fromisoformat(str(payload["start_date"]))
        horizon = int(payload["horizon"])
        items = payload["items"]

        if restaurant <= 0:
            raise ValueError("restaurant must be a positive integer")

        if not 1 <= horizon <= 60:
            raise ValueError("horizon must be between 1 and 60 days")

        if not isinstance(items, list) or not items:
            raise ValueError("items must be a non-empty list")

        if len(items) > 500:
            raise ValueError("Maximum 500 items per batch")

    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    results = []
    seen_item_ids = set()
    successful_items = 0
    failed_items = 0

    required_dates = {
        start_date - timedelta(days=offset)
        for offset in range(1, 29)
    }

    for index, item in enumerate(items):
        try:
            if not isinstance(item, dict):
                raise ValueError("Item must be a JSON object")

            item_id = int(item["item_id"])
            history_rows = item["history"]
            item_name = item.get("item_name")

            if item_id <= 0:
                raise ValueError("item_id must be a positive integer")

            if item_id in seen_item_ids:
                raise ValueError(f"Duplicate item_id: {item_id}")

            seen_item_ids.add(item_id)

            if not isinstance(history_rows, list) or not history_rows:
                raise ValueError("history must be a non-empty list")

            demand_history: dict[date, float] = {}

            for row_index, row in enumerate(history_rows):
                if not isinstance(row, dict):
                    raise ValueError(
                        f"History row {row_index} must be an object"
                    )

                if "date" not in row or "demand_quantity" not in row:
                    raise ValueError(
                        f"History row {row_index} requires date "
                        "and demand_quantity"
                    )

                historical_date = date.fromisoformat(str(row["date"]))
                quantity = float(row["demand_quantity"])

                if not math.isfinite(quantity) or quantity < 0:
                    raise ValueError(
                        f"Invalid demand quantity in history row {row_index}"
                    )

                if historical_date >= start_date:
                    raise ValueError(
                        "History must contain dates before start_date only"
                    )

                demand_history[historical_date] = (
                    demand_history.get(historical_date, 0.0) + quantity
                )

            missing_dates = sorted(
                day.isoformat()
                for day in required_dates
                if day not in demand_history
            )

            if missing_dates:
                raise ValueError(
                    "Missing required historical dates: "
                    + ", ".join(missing_dates[:5])
                    + (
                        f" (and {len(missing_dates) - 5} more)"
                        if len(missing_dates) > 5 else ""
                    )
                )

            state = ForecastState(demand=demand_history)
            predictions = []

            for offset in range(horizon):
                forecast_date = start_date + timedelta(days=offset)

                features = FEATURE_BUILDER.build(
                    forecast_date=forecast_date,
                    restaurant=restaurant,
                    item_id=item_id,
                    state=state,
                )

                predicted_demand = PREDICTION_ADAPTER.predict(features)
                state.add_prediction(forecast_date, predicted_demand)

                predictions.append({
                    "date": forecast_date.isoformat(),
                    "predicted_demand": round(predicted_demand, 4),
                })

            result = {
                "item_id": item_id,
                "status": "success",
                "history_rows_received": len(history_rows),
                "predictions": predictions,
            }

            if item_name is not None:
                result["item_name"] = item_name

            results.append(result)
            successful_items += 1

        except (KeyError, TypeError, ValueError) as exc:
            failed_items += 1
            results.append({
                "item_id": item.get("item_id") if isinstance(item, dict) else None,
                "item_name": item.get("item_name") if isinstance(item, dict) else None,
                "status": "error",
                "error": str(exc),
            })

    return {
        "status": "success" if failed_items == 0 else (
            "partial_success" if successful_items else "failed"
        ),
        "model": MODEL.name,
        "restaurant": restaurant,
        "forecast_start": start_date.isoformat(),
        "horizon_days": horizon,
        "total_items": len(items),
        "successful_items": successful_items,
        "failed_items": failed_items,
        "results": results,
    }

