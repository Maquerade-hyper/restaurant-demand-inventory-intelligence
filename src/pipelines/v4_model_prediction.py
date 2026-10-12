import json
from pathlib import Path

from src.forecasting.model_predictor import ModelPredictor
from src.forecasting.model_registry import ModelRegistry
from src.forecasting.model_trainer import ModelTrainer
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 33 - MODEL PREDICTION")
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

    trainer = ModelTrainer(registry)

    model = trainer.train(
        "ridge",
        train_rows,
        alpha=100.0,
    )

    predictor = ModelPredictor()

    predictions = predictor.predict(
        model,
        validation_rows,
    )

    print()
    print(f"Model:                  {model.name}")
    print(f"Input rows:             {len(validation_rows):,}")
    print(f"Predictions:            {len(predictions):,}")
    print(
        f"Minimum prediction:    "
        f"{min(predictions):.6f}"
    )
    print(
        f"Maximum prediction:    "
        f"{max(predictions):.6f}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()