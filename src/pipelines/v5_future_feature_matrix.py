from datetime import date

from src.forecasting.future_calendar_features import (
    FutureCalendarFeatureBuilder,
)
from src.forecasting.future_feature_matrix import (
    FutureFeatureMatrixBuilder,
)
from src.forecasting.future_lag_features import (
    FutureLagFeatureBuilder,
)
from src.forecasting.future_rolling_features import (
    FutureRollingFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 45 - FUTURE FEATURE MATRIX")
    print("=" * 70)

    forecast_date = date(2026, 9, 15)

    demand_history = {}

    for days_ago in range(1, 29):
        from datetime import timedelta

        historical_date = (
            forecast_date - timedelta(days=days_ago)
        )

        demand_history[historical_date] = float(days_ago)

    calendar_builder = FutureCalendarFeatureBuilder()
    lag_builder = FutureLagFeatureBuilder()
    rolling_builder = FutureRollingFeatureBuilder()
    matrix_builder = FutureFeatureMatrixBuilder()

    calendar = calendar_builder.build(forecast_date)

    lags = lag_builder.build(
        forecast_date=forecast_date,
        demand_history=demand_history,
    )

    rolling = rolling_builder.build(
        forecast_date=forecast_date,
        demand_history=demand_history,
    )

    row = matrix_builder.build(
        restaurant=20,
        item_id=305,
        calendar=calendar,
        lags=lags,
        rolling=rolling,
    )

    print()
    print(f"Date:                   {row.date}")
    print(f"Restaurant:             {row.restaurant}")
    print(f"Item ID:                {row.item_id}")
    print(f"Lag 1:                  {row.lag_1}")
    print(f"Lag 7:                  {row.lag_7}")
    print(f"Rolling mean 7:         {row.rolling_mean_7}")
    print(f"Rolling mean 14:        {row.rolling_mean_14}")
    print(f"Rolling mean 28:        {row.rolling_mean_28}")
    print(f"Rolling max 7:          {row.rolling_max_7}")
    print(f"Rolling std 7:          {row.rolling_std_7}")
    print(f"Day of week:            {row.day_of_week}")
    print(f"Day of month:           {row.day_of_month}")
    print(f"Month:                  {row.month}")
    print(f"Is weekend:             {row.is_weekend}")
    print()

    feature_count = 13

    features = [
        row.lag_1,
        row.lag_7,
        row.lag_14,
        row.lag_28,
        row.rolling_mean_7,
        row.rolling_mean_14,
        row.rolling_mean_28,
        row.rolling_max_7,
        row.rolling_std_7,
        row.day_of_week,
        row.day_of_month,
        row.month,
        row.is_weekend,
    ]

    assert len(features) == feature_count
    assert row.restaurant == 20
    assert row.item_id == 305

    print(f"Feature count:          {len(features)}")
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()