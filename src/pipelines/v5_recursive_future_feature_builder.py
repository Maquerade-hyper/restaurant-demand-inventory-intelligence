from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState
from src.forecasting.recursive_future_feature_builder import (
    RecursiveFutureFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 50 - RECURSIVE FUTURE FEATURE BUILDER")
    print("=" * 70)

    forecast_start = date(2026, 9, 1)

    history = {
        forecast_start - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    state = ForecastState(demand=history.copy())

    builder = RecursiveFutureFeatureBuilder()

    first_row = builder.build(
        forecast_date=date(2026, 9, 1),
        restaurant=20,
        item_id=305,
        state=state,
    )

    print()
    print(f"Forecast date:          {first_row.date}")
    print(f"Restaurant:             {first_row.restaurant}")
    print(f"Item ID:                {first_row.item_id}")
    print(f"Lag 1:                  {first_row.lag_1}")
    print(f"Lag 7:                  {first_row.lag_7}")
    print(f"Lag 14:                 {first_row.lag_14}")
    print(f"Lag 28:                 {first_row.lag_28}")
    print(f"Rolling mean 7:         {first_row.rolling_mean_7}")
    print(f"Rolling mean 14:        {first_row.rolling_mean_14}")
    print(f"Rolling mean 28:        {first_row.rolling_mean_28}")
    print(f"Rolling max 7:          {first_row.rolling_max_7}")
    print(f"Rolling std 7:          {first_row.rolling_std_7}")
    print(f"Day of week:            {first_row.day_of_week}")
    print(f"Day of month:           {first_row.day_of_month}")
    print(f"Month:                  {first_row.month}")
    print(f"Is weekend:             {first_row.is_weekend}")
    print()

    assert first_row.lag_1 == 1.0
    assert first_row.lag_7 == 7.0
    assert first_row.lag_14 == 14.0
    assert first_row.lag_28 == 28.0

    assert first_row.rolling_mean_7 == 4.0
    assert first_row.rolling_mean_14 == 7.5
    assert first_row.rolling_mean_28 == 14.5
    assert first_row.rolling_max_7 == 7.0

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()