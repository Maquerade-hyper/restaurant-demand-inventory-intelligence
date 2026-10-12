from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from statistics import mean, pstdev


@dataclass(frozen=True)
class FutureRollingFeatures:
    date: date
    rolling_mean_7: float
    rolling_mean_14: float
    rolling_mean_28: float
    rolling_max_7: float
    rolling_std_7: float


class FutureRollingFeatureBuilder:
    def build(
        self,
        forecast_date: date,
        demand_history: dict[date, float],
    ) -> FutureRollingFeatures:

        required_dates = [
            forecast_date - timedelta(days=days)
            for days in range(1, 29)
        ]

        missing = [
            historical_date
            for historical_date in required_dates
            if historical_date not in demand_history
        ]

        if missing:
            raise ValueError(
                "Missing historical demand required "
                "for rolling features"
            )

        values_7 = [
            demand_history[
                forecast_date - timedelta(days=days)
            ]
            for days in range(1, 8)
        ]

        values_14 = [
            demand_history[
                forecast_date - timedelta(days=days)
            ]
            for days in range(1, 15)
        ]

        values_28 = [
            demand_history[
                forecast_date - timedelta(days=days)
            ]
            for days in range(1, 29)
        ]

        return FutureRollingFeatures(
            date=forecast_date,
            rolling_mean_7=mean(values_7),
            rolling_mean_14=mean(values_14),
            rolling_mean_28=mean(values_28),
            rolling_max_7=max(values_7),
            rolling_std_7=pstdev(values_7),
        )