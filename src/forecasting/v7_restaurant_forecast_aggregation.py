from __future__ import annotations

from collections import defaultdict

from src.forecasting.v7_forecast_types import ForecastPoint


class RestaurantForecastAggregator:
    def aggregate(
        self,
        points: list[ForecastPoint] | tuple[ForecastPoint, ...],
    ) -> dict[int, float]:
        totals: dict[int, float] = defaultdict(float)

        for point in points:
            totals[point.restaurant] += point.prediction

        return dict(totals)
