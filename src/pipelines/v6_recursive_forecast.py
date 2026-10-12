from datetime import date, timedelta

from src.forecasting.forecast_result_validator import (
    ForecastResultValidator,
)
from src.forecasting.forecast_run_store import ForecastRunJsonStore
from src.forecasting.forecast_state import ForecastState
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_forecast_service import (
    RecursiveForecastService,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V6 - RECURSIVE FORECAST EXECUTION")
    print("=" * 70)

    start = date(2026, 9, 1)

    history = {
        start - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    state = ForecastState(
        demand=history.copy()
    )

    adapter = PredictionAdapter(
        lambda features: (
            features.rolling_mean_7
            + features.lag_1
        ) / 2.0
    )

    service = RecursiveForecastService(adapter)

    result = service.forecast(
        start_date=start,
        horizon=7,
        restaurant=20,
        item_id=305,
        state=state,
    )

    ForecastResultValidator().validate(result)

    output_path = ForecastRunJsonStore().save(
        result,
        "data/features/v6_recursive_forecast.json",
    )

    print()
    print(f"Restaurant:             {result.restaurant}")
    print(f"Item ID:                {result.item_id}")
    print(f"Start date:             {result.start_date}")
    print(f"Horizon:                {result.horizon}")
    print()

    for prediction in result.predictions:
        print(
            f"{prediction.date} -> "
            f"{prediction.prediction}"
        )

    print()
    print(f"Total prediction:      {result.total_prediction}")
    print(f"Output:                 {output_path}")
    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()
