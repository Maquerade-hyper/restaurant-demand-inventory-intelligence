from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class FutureLagFeatures:
    date: date
    lag_1: float
    lag_7: float
    lag_14: float
    lag_28: float


class FutureLagFeatureBuilder:
    def build(
        self,
        forecast_date: date,
        demand_history: dict[date, float],
    ) -> FutureLagFeatures:

        required_dates = {
            "lag_1": forecast_date - timedelta(days=1),
            "lag_7": forecast_date - timedelta(days=7),
            "lag_14": forecast_date - timedelta(days=14),
            "lag_28": forecast_date - timedelta(days=28),
        }

        missing = [
            name
            for name, historical_date in required_dates.items()
            if historical_date not in demand_history
        ]

        if missing:
            raise ValueError(
                f"Missing historical demand for: {', '.join(missing)}"
            )

        return FutureLagFeatures(
            date=forecast_date,
            lag_1=demand_history[required_dates["lag_1"]],
            lag_7=demand_history[required_dates["lag_7"]],
            lag_14=demand_history[required_dates["lag_14"]],
            lag_28=demand_history[required_dates["lag_28"]],
        )