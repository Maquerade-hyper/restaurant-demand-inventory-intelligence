from __future__ import annotations

from datetime import date

from src.forecasting.forecast_state import ForecastState
from src.forecasting.prediction_adapter import PredictionAdapter
from src.forecasting.recursive_forecast_types import RecursivePrediction
from src.forecasting.recursive_future_feature_builder import (
    RecursiveFutureFeatureBuilder,
)


class RecursiveForecastStep:
    def __init__(
        self,
        feature_builder: RecursiveFutureFeatureBuilder | None = None,
        prediction_adapter: PredictionAdapter | None = None,
    ) -> None:
        self.feature_builder = (
            feature_builder or RecursiveFutureFeatureBuilder()
        )

        if prediction_adapter is None:
            raise ValueError(
                "prediction_adapter is required"
            )

        self.prediction_adapter = prediction_adapter

    def execute(
        self,
        forecast_date: date,
        restaurant: int,
        item_id: int,
        state: ForecastState,
    ) -> RecursivePrediction:
        features = self.feature_builder.build(
            forecast_date=forecast_date,
            restaurant=restaurant,
            item_id=item_id,
            state=state,
        )

        prediction = self.prediction_adapter.predict(features)

        state.add_prediction(
            forecast_date,
            prediction,
        )

        return RecursivePrediction(
            date=forecast_date,
            restaurant=restaurant,
            item_id=item_id,
            prediction=prediction,
        )
