from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FutureFeatureRow:
    date: date
    restaurant: int
    item_id: int


class FutureFeatureBuilder:
    def build(
        self,
        dates: list[date],
        restaurant: int,
        item_id: int,
    ) -> list[FutureFeatureRow]:

        if not dates:
            raise ValueError(
                "Future dates must not be empty"
            )

        if restaurant <= 0:
            raise ValueError(
                "Restaurant ID must be greater than 0"
            )

        if item_id <= 0:
            raise ValueError(
                "Item ID must be greater than 0"
            )

        return [
            FutureFeatureRow(
                date=forecast_date,
                restaurant=restaurant,
                item_id=item_id,
            )
            for forecast_date in dates
        ]