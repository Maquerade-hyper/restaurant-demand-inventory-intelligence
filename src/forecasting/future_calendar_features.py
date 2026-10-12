from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FutureCalendarFeatures:
    date: date
    day_of_week: int
    day_of_month: int
    month: int
    is_weekend: int


class FutureCalendarFeatureBuilder:
    def build(
        self,
        forecast_date: date,
    ) -> FutureCalendarFeatures:

        return FutureCalendarFeatures(
            date=forecast_date,
            day_of_week=forecast_date.weekday(),
            day_of_month=forecast_date.day,
            month=forecast_date.month,
            is_weekend=int(forecast_date.weekday() >= 5),
        )