import json
from pathlib import Path

from src.forecasting.metrics import evaluate
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)

OUTPUT_PATH = Path(
    "data/features/ridge_segment_evaluation.json"
)

REPORT_PATH = Path(
    "data/reports/ridge_segment_evaluation.json"
)


def evaluate_segment(
    actuals: list[float],
    predictions: list[float],
) -> dict:
    metrics = evaluate(
        actuals,
        predictions,
    )

    return {
        "count": len(actuals),
        "mae": metrics["mae"],
        "rmse": metrics["rmse"],
        "smape": metrics["smape"],
    }


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 28 - RIDGE SEGMENT EVALUATION")
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

    zero_indices = [
        index
        for index, value in enumerate(actuals)
        if value == 0
    ]

    positive_indices = [
        index
        for index, value in enumerate(actuals)
        if value > 0
    ]

    zero_actuals = [
        actuals[index]
        for index in zero_indices
    ]

    zero_predictions = [
        predictions[index]
        for index in zero_indices
    ]

    positive_actuals = [
        actuals[index]
        for index in positive_indices
    ]

    positive_predictions = [
        predictions[index]
        for index in positive_indices
    ]

    results = {
        "all": evaluate_segment(
            actuals,
            predictions,
        ),
        "zero_actual": evaluate_segment(
            zero_actuals,
            zero_predictions,
        ),
        "positive_actual": evaluate_segment(
            positive_actuals,
            positive_predictions,
        ),
    }

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
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 28",
        "description": (
            "Segment-aware Ridge evaluation"
        ),
        "model": model.name,
        "alpha": model.alpha,
        "validation_rows": len(validation_rows),
        "results": results,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    for segment in (
        "all",
        "zero_actual",
        "positive_actual",
    ):
        metrics = results[segment]

        print()
        print(f"[{segment}]")
        print(
            f"  count={metrics['count']}"
        )
        print(
            f"  MAE={metrics['mae']:.6f}"
        )
        print(
            f"  RMSE={metrics['rmse']:.6f}"
        )
        print(
            f"  sMAPE={metrics['smape']:.6f}%"
        )

    print()
    print(
        f"Feature output:        "
        f"{OUTPUT_PATH.resolve()}"
    )
    print(
        f"Report:                "
        f"{REPORT_PATH.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()