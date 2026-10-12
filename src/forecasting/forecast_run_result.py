from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.forecasting.recursive_forecast_types import RecursivePrediction


@dataclass(frozen=True)
class ForecastRunResult:
    restaurant: int
    item_id: int
    start_date: date
    horizon: int
    predictions: tuple[RecursivePrediction, ...]

    @property
    def total_prediction(self) -> float:
        return sum(
            prediction.prediction
            for prediction in self.predictions
        )
