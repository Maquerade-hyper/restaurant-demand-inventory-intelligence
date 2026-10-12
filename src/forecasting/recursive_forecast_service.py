from __future__ import annotations

from datetime import date

from src.forecasting.forecast_run_result import ForecastRunResult
from src.forecasting.forecast_state import ForecastState
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_forecast_types import RecursivePrediction
from src.forecasting.recursive_horizon_executor import (
    RecursiveHorizonExecutor,
)


class RecursiveForecastService:
    def __init__(
        self,
        prediction_adapter: PredictionAdapter,
    ) -> None:
        self.executor = RecursiveHorizonExecutor(
            prediction_adapter=prediction_adapter,
        )

    def forecast(
        self,
        start_date: date,
        horizon: int,
        restaurant: int,
        item_id: int,
        state: ForecastState,
    ) -> ForecastRunResult:
        predictions = self.executor.execute(
            start_date=start_date,
            horizon=horizon,
            restaurant=restaurant,
            item_id=item_id,
            state=state,
        )

        return ForecastRunResult(
            restaurant=restaurant,
            item_id=item_id,
            start_date=start_date,
            horizon=horizon,
            predictions=tuple(predictions),
        )
