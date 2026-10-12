from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ForecastRequest:
    restaurant: int
    item_id: int
    start_date: date
    horizon_days: int


class ForecastRequestBuilder:
    def build(
        self,
        restaurant: int,
        item_id: int,
        start_date: date,
        horizon_days: int,
    ) -> ForecastRequest:

        if restaurant <= 0:
            raise ValueError(
                "Restaurant ID must be greater than 0"
            )

        if item_id <= 0:
            raise ValueError(
                "Item ID must be greater than 0"
            )

        if horizon_days <= 0:
            raise ValueError(
                "Forecast horizon must be greater than 0"
            )

        return ForecastRequest(
            restaurant=restaurant,
            item_id=item_id,
            start_date=start_date,
            horizon_days=horizon_days,
        )