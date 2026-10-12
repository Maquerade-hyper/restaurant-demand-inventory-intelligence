from datetime import date, timedelta

from src.forecasting.forecast_result_validator import (
    ForecastResultValidator,
)
from src.forecasting.forecast_run_result import ForecastRunResult
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_forecast_service import (
    RecursiveForecastService,
)
from src.forecasting.recursive_forecast_types import (
    RecursivePrediction,
)
from src.forecasting.forecast_state import ForecastState
from src.forecasting.v7_forecast_package_store import (
    ForecastPackageStore,
)
from src.forecasting.v7_forecast_processing_service import (
    ForecastProcessingService,
)
from src.forecasting.v7_item_forecast_aggregation import (
    ItemForecastAggregator,
)
from src.forecasting.v7_restaurant_forecast_aggregation import (
    RestaurantForecastAggregator,
)
from src.forecasting.v7_overall_forecast_aggregation import (
    OverallForecastAggregator,
)


def make_state(start: date) -> ForecastState:
    history = {
        start - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    return ForecastState(
        demand=history
    )


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V7 - FORECAST RESULT PROCESSING")
    print("=" * 70)

    start = date(2026, 9, 1)

    adapter = PredictionAdapter(
        lambda features: (
            features.rolling_mean_7
            + features.lag_1
        ) / 2.0
    )

    service = RecursiveForecastService(
        prediction_adapter=adapter
    )

    validator = ForecastResultValidator()

    results = []

    configurations = [
        (20, 305),
        (20, 306),
        (21, 305),
    ]

    for restaurant, item_id in configurations:
        state = make_state(start)

        result = service.forecast(
            start_date=start,
            horizon=7,
            restaurant=restaurant,
            item_id=item_id,
            state=state,
        )

        validator.validate(result)
        results.append(result)

    processing = ForecastProcessingService()

    package = processing.process(results)

    all_points = tuple(
        point
        for series in package.series
        for point in series.points
    )

    item_totals = ItemForecastAggregator().aggregate(
        all_points
    )

    restaurant_totals = RestaurantForecastAggregator().aggregate(
        all_points
    )

    overall_total = OverallForecastAggregator().aggregate(
        all_points
    )

    output = ForecastPackageStore().save(
        package,
        "data/features/v7_forecast_package.json",
    )

    print()
    print(f"Start date:             {package.start_date}")
    print(f"Horizon:                {package.horizon}")
    print(f"Forecast series:        {len(package.series)}")
    print(f"Forecast points:        {len(all_points)}")
    print()

    print("ITEM TOTALS")
    for item_id, total in sorted(item_totals.items()):
        print(
            f"Item {item_id}:              {total}"
        )

    print()
    print("RESTAURANT TOTALS")
    for restaurant, total in sorted(
        restaurant_totals.items()
    ):
        print(
            f"Restaurant {restaurant}:         {total}"
        )

    print()
    print(f"Overall forecast:       {overall_total}")
    print(f"Output:                 {output}")
    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()
