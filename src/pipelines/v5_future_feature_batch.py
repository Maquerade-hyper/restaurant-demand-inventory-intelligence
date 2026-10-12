from datetime import date, timedelta

from src.forecasting.future_calendar_features import (
    FutureCalendarFeatureBuilder,
)
from src.forecasting.future_feature_batch import (
    FutureFeatureBatchBuilder,
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
    print("V5 PART 46 - FUTURE FEATURE BATCH")
    print("=" * 70)

    forecast_date = date(2026, 9, 15)

    demand_history = {
        forecast_date - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    calendar_builder = FutureCalendarFeatureBuilder()
    lag_builder = FutureLagFeatureBuilder()
    rolling_builder = FutureRollingFeatureBuilder()
    matrix_builder = FutureFeatureMatrixBuilder()
    batch_builder = FutureFeatureBatchBuilder()

    calendar = calendar_builder.build(
        forecast_date
    )

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

    batch = batch_builder.build(
        rows=[row]
    )

    print()
    print(f"Rows:                   {len(batch.rows)}")
    print(f"First date:             {batch.rows[0].date}")
    print(f"Last date:              {batch.rows[-1].date}")
    print(f"Restaurant:             {batch.rows[0].restaurant}")
    print(f"Item ID:                {batch.rows[0].item_id}")
    print()
    print(
        "STATUS: PASSED"
    )


if __name__ == "__main__":
    main()