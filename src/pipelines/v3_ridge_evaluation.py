import json
from pathlib import Path

from src.forecasting.metrics import evaluate
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)

OUTPUT_PATH = Path(
    "data/features/ridge_predictions.json"
)

REPORT_PATH = Path(
    "data/reports/ridge_evaluation.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 27 - RIDGE MODEL EVALUATION")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )

    train_rows = payload["train"]
    validation_rows = payload["validation"]

    model = RidgeDemandModel(alpha=1.0)

    model.fit(train_rows)

    predictions = model.predict(
        validation_rows
    )

    actuals = [
        float(row["demand_quantity"])
        for row in validation_rows
    ]

    metrics = evaluate(
        actuals,
        predictions,
    )

    prediction_rows = []

    for row, prediction in zip(
        validation_rows,
        predictions,
    ):
        prediction_rows.append(
            {
                "date": row["date"],
                "restaurant": row["restaurant"],
                "item_id": row["item_id"],
                "actual": float(
                    row["demand_quantity"]
                ),
                "predicted": float(prediction),
            }
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "model": model.name,
                "alpha": model.alpha,
                "predictions": prediction_rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 27",
        "description": "Ridge demand model evaluation",
        "model": model.name,
        "alpha": model.alpha,
        "train_rows": len(train_rows),
        "validation_rows": len(validation_rows),
        "mae": metrics["mae"],
        "rmse": metrics["rmse"],
        "smape": metrics["smape"],
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Model:                  {model.name}")
    print(f"Alpha:                  {model.alpha}")
    print(f"Training rows:          {len(train_rows):,}")
    print(
        f"Validation rows:       "
        f"{len(validation_rows):,}"
    )

    print()
    print(
        f"MAE:                    "
        f"{metrics['mae']:.6f}"
    )
    print(
        f"RMSE:                   "
        f"{metrics['rmse']:.6f}"
    )
    print(
        f"sMAPE:                  "
        f"{metrics['smape']:.6f}%"
    )

    print()
    print(
        f"Predictions:            "
        f"{OUTPUT_PATH.resolve()}"
    )
    print(
        f"Report:                 "
        f"{REPORT_PATH.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()