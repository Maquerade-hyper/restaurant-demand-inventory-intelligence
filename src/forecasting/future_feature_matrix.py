from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.forecasting.future_calendar_features import (
    FutureCalendarFeatures,
)
from src.forecasting.future_lag_features import (
    FutureLagFeatures,
)
from src.forecasting.future_rolling_features import (
    FutureRollingFeatures,
)


@dataclass(frozen=True)
class FutureFeatureMatrixRow:
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


class FutureFeatureMatrixBuilder:
    def build(
        self,
        restaurant: int,
        item_id: int,
        calendar: FutureCalendarFeatures,
        lags: FutureLagFeatures,
        rolling: FutureRollingFeatures,
    ) -> FutureFeatureMatrixRow:

        if restaurant <= 0:
            raise ValueError(
                "Restaurant ID must be greater than 0"
            )

        if item_id <= 0:
            raise ValueError(
                "Item ID must be greater than 0"
            )

        if calendar.date != lags.date:
            raise ValueError(
                "Calendar and lag dates must match"
            )

        if calendar.date != rolling.date:
            raise ValueError(
                "Calendar and rolling dates must match"
            )

        return FutureFeatureMatrixRow(
            date=calendar.date,
            restaurant=restaurant,
            item_id=item_id,
            lag_1=lags.lag_1,
            lag_7=lags.lag_7,
            lag_14=lags.lag_14,
            lag_28=lags.lag_28,
            rolling_mean_7=rolling.rolling_mean_7,
            rolling_mean_14=rolling.rolling_mean_14,
            rolling_mean_28=rolling.rolling_mean_28,
            rolling_max_7=rolling.rolling_max_7,
            rolling_std_7=rolling.rolling_std_7,
            day_of_week=calendar.day_of_week,
            day_of_month=calendar.day_of_month,
            month=calendar.month,
            is_weekend=calendar.is_weekend,
        )