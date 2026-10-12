import json
from pathlib import Path

from src.forecasting.metrics import evaluate
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)

OUTPUT_PATH = Path(
    "data/features/ridge_hyperparameters.json"
)

REPORT_PATH = Path(
    "data/reports/ridge_hyperparameters.json"
)


ALPHAS = [
    0.01,
    0.1,
    1.0,
    10.0,
    100.0,
]


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 29 - RIDGE HYPERPARAMETERS")
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

    actuals = [
        float(row["demand_quantity"])
        for row in validation_rows
    ]

    results = []

    for alpha in ALPHAS:
        model = RidgeDemandModel(
            alpha=alpha
        )

        model.fit(train_rows)

        predictions = model.predict(
            validation_rows
        )

        metrics = evaluate(
            actuals,
            predictions,
        )

        result = {
            "model": model.name,
            "alpha": alpha,
            "mae": metrics["mae"],
            "rmse": metrics["rmse"],
            "smape": metrics["smape"],
        }

        results.append(result)

        print()
        print(f"alpha={alpha}")
        print(
            f"  MAE={metrics['mae']:.6f}"
        )
        print(
            f"  RMSE={metrics['rmse']:.6f}"
        )
        print(
            f"  sMAPE={metrics['smape']:.6f}%"
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
                "model": "ridge",
                "alphas": ALPHAS,
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 29",
        "description": (
            "Ridge regularization evaluation"
        ),
        "train_rows": len(train_rows),
        "validation_rows": len(validation_rows),
        "alphas": ALPHAS,
        "results": results,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
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