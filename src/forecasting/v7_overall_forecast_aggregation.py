from __future__ import annotations

from src.forecasting.v7_forecast_types import ForecastPoint


class OverallForecastAggregator:
    def aggregate(
        self,
        points: list[ForecastPoint] | tuple[ForecastPoint, ...],
    ) -> float:
        return sum(
            point.prediction
            for point in points
        )
