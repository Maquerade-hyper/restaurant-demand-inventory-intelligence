from __future__ import annotations

from statistics import mean, median, pstdev

from src.forecasting.v8_forecast_distribution import (
    ForecastDistribution,
)


class ForecastStatistics:
    def calculate(
        self,
        distribution: ForecastDistribution,
    ) -> dict[str, float]:
        if not distribution.values:
            raise ValueError(
                "forecast distribution cannot be empty"
            )

        return {
            "mean": mean(distribution.values),
            "median": median(distribution.values),
            "std": pstdev(distribution.values),
            "minimum": distribution.minimum,
            "maximum": distribution.maximum,
            "total": distribution.total,
        }
