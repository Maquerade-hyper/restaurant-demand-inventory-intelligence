from __future__ import annotations

from datetime import date, timedelta
from statistics import mean, pstdev

from src.forecasting.forecast_state import ForecastState


class RecursiveRollingResolver:
    def resolve(
        self,
        forecast_date: date,
        state: ForecastState,
    ) -> dict[str, float]:

        values_7 = [
            state.get_demand(
                forecast_date - timedelta(days=days)
            )
            for days in range(1, 8)
        ]

        values_14 = [
            state.get_demand(
                forecast_date - timedelta(days=days)
            )
            for days in range(1, 15)
        ]

        values_28 = [
            state.get_demand(
                forecast_date - timedelta(days=days)
            )
            for days in range(1, 29)
        ]

        return {
            "rolling_mean_7": mean(values_7),
            "rolling_mean_14": mean(values_14),
            "rolling_mean_28": mean(values_28),
            "rolling_max_7": max(values_7),
            "rolling_std_7": pstdev(values_7),
        }