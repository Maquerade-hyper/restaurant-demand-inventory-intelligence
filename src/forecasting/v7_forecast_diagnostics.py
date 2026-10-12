from __future__ import annotations

from dataclasses import dataclass

from src.forecasting.v7_forecast_types import ForecastSeries


@dataclass(frozen=True)
class ForecastDiagnostics:
    horizon: int
    zero_prediction_count: int
    positive_prediction_count: int
    total_prediction: float
    minimum_prediction: float
    maximum_prediction: float


class ForecastDiagnosticsBuilder:
    def build(
        self,
        series: ForecastSeries,
    ) -> ForecastDiagnostics:
        values = [
            point.prediction
            for point in series.points
        ]

        zero_count = sum(
            1
            for value in values
            if value == 0
        )

        positive_count = sum(
            1
            for value in values
            if value > 0
        )

        return ForecastDiagnostics(
            horizon=len(values),
            zero_prediction_count=zero_count,
            positive_prediction_count=positive_count,
            total_prediction=sum(values),
            minimum_prediction=min(values) if values else 0.0,
            maximum_prediction=max(values) if values else 0.0,
        )
