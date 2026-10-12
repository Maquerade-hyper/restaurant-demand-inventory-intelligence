import json
from dataclasses import asdict
from pathlib import Path

from src.forecasting.forecast_results import (
    ForecastResultBuilder,
)
from src.forecasting.forecast_service import (
    ForecastService,
)
from src.forecasting.model_registry import ModelRegistry
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)

OUTPUT_PATH = Path(
    "data/features/forecast_results.json"
)

REPORT_PATH = Path(
    "data/reports/forecast_results.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 35 - FORECAST RESULTS")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(
            encoding="utf-8"
        )
    )

    train_rows = payload["train"]
    validation_rows = payload["validation"]

    registry = ModelRegistry()
    registry.register(RidgeDemandModel)

    service = ForecastService(registry)

    predictions = service.train_and_predict(
        "ridge",
        train_rows,
        validation_rows,
        alpha=100.0,
    )

    builder = ForecastResultBuilder()

    results = builder.build(
        validation_rows,
        predictions,
    )

    serialized = [
        asdict(result)
        for result in results
    ]

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
                "results": serialized,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V4 Part 35",
        "description": (
            "Forecast result construction"
        ),
        "model": "ridge",
        "input_rows": len(validation_rows),
        "result_rows": len(results),
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("Model:                  ridge")
    print(
        f"Validation rows:       "
        f"{len(validation_rows):,}"
    )
    print(
        f"Forecast results:      "
        f"{len(results):,}"
    )

    if results:
        first = results[0]

        print()
        print("First result:")
        print(
            f"  date={first.date}"
        )
        print(
            f"  restaurant={first.restaurant}"
        )
        print(
            f"  item_id={first.item_id}"
        )
        print(
            f"  actual={first.actual:.6f}"
        )
        print(
            f"  predicted={first.predicted:.6f}"
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