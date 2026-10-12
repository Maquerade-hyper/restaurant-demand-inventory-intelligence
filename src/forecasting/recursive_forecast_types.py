from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RecursivePrediction:
    date: date
    restaurant: int
    item_id: int
    prediction: float


@dataclass(frozen=True)
class RecursiveForecastRun:
    restaurant: int
    item_id: int
    start_date: date
    horizon: int
    predictions: tuple[RecursivePrediction, ...]
