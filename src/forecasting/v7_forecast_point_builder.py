from __future__ import annotations

from src.forecasting.forecast_run_result import ForecastRunResult
from src.forecasting.v7_forecast_types import (
    ForecastPoint,
    ForecastSeries,
)


class ForecastPointBuilder:
    def build(
        self,
        result: ForecastRunResult,
    ) -> ForecastSeries:
        points = tuple(
            ForecastPoint(
                date=prediction.date,
                restaurant=prediction.restaurant,
                item_id=prediction.item_id,
                prediction=prediction.prediction,
            )
            for prediction in result.predictions
        )

        return ForecastSeries(
            restaurant=result.restaurant,
            item_id=result.item_id,
            points=points,
        )
