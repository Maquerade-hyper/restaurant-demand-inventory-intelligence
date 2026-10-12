import json
from pathlib import Path

from src.forecasting.model_registry import ModelRegistry
from src.forecasting.model_trainer import ModelTrainer
from src.forecasting.ridge_model import RidgeDemandModel


INPUT_PATH = Path(
    "data/features/training_split.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 32 - MODEL TRAINING")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )

    train_rows = payload["train"]

    registry = ModelRegistry()
    registry.register(RidgeDemandModel)

    trainer = ModelTrainer(registry)

    model = trainer.train(
        "ridge",
        train_rows,
        alpha=100.0,
    )

    print()
    print(
        f"Model:                  "
        f"{model.name}"
    )
    print(
        f"Training rows:          "
        f"{len(train_rows):,}"
    )
    print(
        f"Alpha:                  "
        f"{model.alpha}"
    )
    print(
        f"Fitted:                 "
        f"{model.fitted}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()
    