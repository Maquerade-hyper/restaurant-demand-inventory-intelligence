from datetime import date, timedelta

from src.forecasting.future_lag_features import (
    FutureLagFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 43 - FUTURE LAG FEATURES")
    print("=" * 70)

    forecast_date = date(2026, 9, 15)

    demand_history = {}

    for days_ago in range(1, 29):
        historical_date = forecast_date - timedelta(days=days_ago)
        demand_history[historical_date] = float(days_ago)

    builder = FutureLagFeatureBuilder()

    features = builder.build(
        forecast_date=forecast_date,
        demand_history=demand_history,
    )

    print()
    print(f"Forecast date:          {features.date}")
    print(f"Lag 1:                  {features.lag_1}")
    print(f"Lag 7:                  {features.lag_7}")
    print(f"Lag 14:                 {features.lag_14}")
    print(f"Lag 28:                 {features.lag_28}")
    print()

    assert features.lag_1 == 1.0
    assert features.lag_7 == 7.0
    assert features.lag_14 == 14.0
    assert features.lag_28 == 28.0

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()