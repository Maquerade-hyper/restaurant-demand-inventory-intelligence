from __future__ import annotations

from dataclasses import dataclass

from src.forecasting.v7_forecast_types import ForecastSeries


@dataclass(frozen=True)
class ForecastHorizonSummary:
    horizon: int
    total_prediction: float
    minimum_prediction: float
    maximum_prediction: float
    average_prediction: float


class ForecastHorizonSummarizer:
    def summarize(
        self,
        series: ForecastSeries,
    ) -> ForecastHorizonSummary:
        if not series.points:
            raise ValueError("forecast series cannot be empty")

        values = [
            point.prediction
            for point in series.points
        ]

        return ForecastHorizonSummary(
            horizon=len(values),
            total_prediction=sum(values),
            minimum_prediction=min(values),
            maximum_prediction=max(values),
            average_prediction=sum(values) / len(values),
        )
