from datetime import date, timedelta

from src.forecasting.future_rolling_features import (
    FutureRollingFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 44 - FUTURE ROLLING FEATURES")
    print("=" * 70)

    forecast_date = date(2026, 9, 15)

    demand_history = {}

    for days_ago in range(1, 29):
        historical_date = (
            forecast_date - timedelta(days=days_ago)
        )
        demand_history[historical_date] = float(days_ago)

    builder = FutureRollingFeatureBuilder()

    features = builder.build(
        forecast_date=forecast_date,
        demand_history=demand_history,
    )

    print()
    print(f"Forecast date:          {features.date}")
    print(f"Rolling mean 7:         {features.rolling_mean_7}")
    print(f"Rolling mean 14:        {features.rolling_mean_14}")
    print(f"Rolling mean 28:        {features.rolling_mean_28}")
    print(f"Rolling max 7:          {features.rolling_max_7}")
    print(f"Rolling std 7:          {features.rolling_std_7}")
    print()

    assert features.rolling_mean_7 == 4.0
    assert features.rolling_mean_14 == 7.5
    assert features.rolling_mean_28 == 14.5
    assert features.rolling_max_7 == 7.0
    assert round(features.rolling_std_7, 6) == 2.0

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()