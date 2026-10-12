from __future__ import annotations

import json
import math
from dataclasses import asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

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
