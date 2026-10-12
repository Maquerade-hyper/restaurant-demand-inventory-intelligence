import json
from pathlib import Path

from src.forecasting.forecast_service import (
    ForecastService,
)
from src.forecasting.model_registry import ModelRegistry
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 34 - FORECAST SERVICE")
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

    registry = ModelRegistry()
    registry.register(RidgeDemandModel)

    service = ForecastService(registry)

    predictions = service.train_and_predict(
        "ridge",
        train_rows,
        validation_rows,
        alpha=100.0,
    )

    print()
    print("Model:                  ridge")
    print(
        f"Training rows:          "
        f"{len(train_rows):,}"
    )
    print(
        f"Prediction rows:        "
        f"{len(validation_rows):,}"
    )
    print(
        f"Predictions generated:  "
        f"{len(predictions):,}"
    )
    print(
        f"Minimum prediction:     "
        f"{min(predictions):.6f}"
    )
    print(
        f"Maximum prediction:     "
        f"{max(predictions):.6f}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()