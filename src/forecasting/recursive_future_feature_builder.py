from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.forecasting.forecast_state import ForecastState
from src.forecasting.recursive_lag_resolver import RecursiveLagResolver
from src.forecasting.recursive_rolling_resolver import (
    RecursiveRollingResolver,
)


@dataclass(frozen=True)
class RecursiveFutureFeatureRow:
    date: date
    restaurant: int
    item_id: int

    lag_1: float
    lag_7: float
    lag_14: float
    lag_28: float

    rolling_mean_7: float
    rolling_mean_14: float
    rolling_mean_28: float
    rolling_max_7: float
    rolling_std_7: float

    day_of_week: int
    day_of_month: int
    month: int
    is_weekend: int


class RecursiveFutureFeatureBuilder:
    def __init__(
        self,
        lag_resolver: RecursiveLagResolver | None = None,
        rolling_resolver: RecursiveRollingResolver | None = None,
    ) -> None:
        self.lag_resolver = lag_resolver or RecursiveLagResolver()
        self.rolling_resolver = (
            rolling_resolver or RecursiveRollingResolver()
        )

    def build(
        self,
        forecast_date: date,
        restaurant: int,
        item_id: int,
        state: ForecastState,
    ) -> RecursiveFutureFeatureRow:
        if restaurant <= 0:
            raise ValueError("restaurant must be positive")

        if item_id <= 0:
            raise ValueError("item_id must be positive")

        lag_features = self.lag_resolver.resolve(
            forecast_date=forecast_date,
            state=state,
        )

        rolling_features = self.rolling_resolver.resolve(
            forecast_date=forecast_date,
            state=state,
        )

        return RecursiveFutureFeatureRow(
            date=forecast_date,
            restaurant=restaurant,
            item_id=item_id,

            lag_1=lag_features["lag_1"],
            lag_7=lag_features["lag_7"],
            lag_14=lag_features["lag_14"],
            lag_28=lag_features["lag_28"],

            rolling_mean_7=rolling_features["rolling_mean_7"],
            rolling_mean_14=rolling_features["rolling_mean_14"],
            rolling_mean_28=rolling_features["rolling_mean_28"],
            rolling_max_7=rolling_features["rolling_max_7"],
            rolling_std_7=rolling_features["rolling_std_7"],

            day_of_week=forecast_date.weekday(),
            day_of_month=forecast_date.day,
            month=forecast_date.month,
            is_weekend=1 if forecast_date.weekday() >= 5 else 0,
        )