from src.forecasting.forecast_horizon import (
    ForecastHorizonBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 37 - FORECAST HORIZON")
    print("=" * 70)

    builder = ForecastHorizonBuilder()

    horizon = builder.build(14)

    print()
    print(
        f"Forecast horizon:      "
        f"{horizon.days} days"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()