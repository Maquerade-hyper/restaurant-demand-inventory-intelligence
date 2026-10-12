from __future__ import annotations

from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState


class RecursiveLagResolver:
    def resolve(
        self,
        forecast_date: date,
        state: ForecastState,
    ) -> dict[str, float]:

        offsets = {
            "lag_1": 1,
            "lag_7": 7,
            "lag_14": 14,
            "lag_28": 28,
        }

        resolved: dict[str, float] = {}

        for name, offset in offsets.items():
            historical_date = (
                forecast_date - timedelta(days=offset)
            )

            resolved[name] = state.get_demand(
                historical_date
            )

        return resolved