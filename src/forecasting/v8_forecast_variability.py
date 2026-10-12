from __future__ import annotations

from dataclasses import dataclass

from src.forecasting.v8_forecast_statistics import (
    ForecastStatistics,
)


@dataclass(frozen=True)
class ForecastVariability:
    standard_deviation: float
    coefficient_of_variation: float


class ForecastVariabilityAnalyzer:
    def analyze(
        self,
        statistics: dict[str, float],
    ) -> ForecastVariability:
        mean_value = statistics["mean"]
        std_value = statistics["std"]

        if mean_value == 0:
            coefficient = 0.0
        else:
            coefficient = std_value / mean_value

        return ForecastVariability(
            standard_deviation=std_value,
            coefficient_of_variation=coefficient,
        )
