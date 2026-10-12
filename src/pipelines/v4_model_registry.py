from src.forecasting.model_registry import ModelRegistry
from src.forecasting.ridge_model import RidgeDemandModel


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 31 - MODEL REGISTRY")
    print("=" * 70)

    registry = ModelRegistry()

    registry.register(RidgeDemandModel)

    print()
    print("Registered models:")

    for name in registry.names():
        model_class = registry.get(name)
        model = model_class()

        print(
            f"  - {name} "
            f"({model_class.__name__})"
        )

    print()
    print(
        f"Model count:            "
        f"{len(registry.names())}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()