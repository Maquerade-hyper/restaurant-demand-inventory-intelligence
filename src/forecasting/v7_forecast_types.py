from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ForecastPoint:
    date: date
    restaurant: int
    item_id: int
    prediction: float


@dataclass(frozen=True)
class ForecastSeries:
    restaurant: int
    item_id: int
    points: tuple[ForecastPoint, ...]

    @property
    def total(self) -> float:
        return sum(point.prediction for point in self.points)


@dataclass(frozen=True)
class ForecastPackage:
    start_date: date
    horizon: int
    series: tuple[ForecastSeries, ...]
