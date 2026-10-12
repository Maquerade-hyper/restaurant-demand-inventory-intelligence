from __future__ import annotations

from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_forecast_step import RecursiveForecastStep
from src.forecasting.recursive_forecast_types import RecursivePrediction


class RecursiveHorizonExecutor:
    def __init__(
        self,
        prediction_adapter: PredictionAdapter,
    ) -> None:
        self.step = RecursiveForecastStep(
            prediction_adapter=prediction_adapter,
        )

    def execute(
        self,
        start_date: date,
        horizon: int,
        restaurant: int,
        item_id: int,
        state: ForecastState,
    ) -> list[RecursivePrediction]:
        if horizon <= 0:
            raise ValueError("horizon must be positive")

        predictions: list[RecursivePrediction] = []

        for offset in range(horizon):
            forecast_date = start_date + timedelta(days=offset)

            prediction = self.step.execute(
                forecast_date=forecast_date,
                restaurant=restaurant,
                item_id=item_id,
                state=state,
            )

            predictions.append(prediction)

        return predictions
