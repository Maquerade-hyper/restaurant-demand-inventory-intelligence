from __future__ import annotations

from datetime import date, timedelta
from typing import Any


class DemandCalendarBuilder:
    """
    Creates a complete daily demand calendar.

    Grain:
        one row per date + restaurant + item_id

    Only item/restaurant combinations already observed
    in the source demand dataset are used.

    Missing demand on an observed calendar date becomes 0.
    """

    def __init__(self, daily_demand: list[dict[str, Any]]):
        self.daily_demand = daily_demand

    @staticmethod
    def _parse_date(value: Any) -> date:
        return date.fromisoformat(str(value))

    def build(self) -> list[dict[str, Any]]:
        if not self.daily_demand:
            return []

        dates = [
            self._parse_date(row["date"])
            for row in self.daily_demand
            if row.get("date") is not None
        ]

        if not dates:
            return []

        start_date = min(dates)
        end_date = max(dates)

        combinations: dict[
            tuple[Any, Any],
            str | None
        ] = {}

        demand_lookup: dict[
            tuple[str, Any, Any],
            dict[str, Any]
        ] = {}

        for row in self.daily_demand:
            item_id = row.get("item_id")
            restaurant = row.get("restaurant")
            row_date = row.get("date")

            if item_id is None or row_date is None:
                continue

            combination = (restaurant, item_id)

            if combination not in combinations:
                combinations[combination] = row.get("item_name")

            key = (str(row_date), restaurant, item_id)

            demand_lookup[key] = row

        result: list[dict[str, Any]] = []

        current_date = start_date

        while current_date <= end_date:
            date_string = current_date.isoformat()

            for (restaurant, item_id), item_name in combinations.items():
                key = (
                    date_string,
                    restaurant,
                    item_id,
                )

                existing = demand_lookup.get(key)

                if existing is None:
                    result.append(
                        {
                            "date": date_string,
                            "restaurant": restaurant,
                            "item_id": item_id,
                            "item_name": item_name,
                            "demand_quantity": 0.0,
                            "order_count": 0,
                        }
                    )
                else:
                    result.append(
                        {
                            "date": date_string,
                            "restaurant": restaurant,
                            "item_id": item_id,
                            "item_name": item_name,
                            "demand_quantity": float(
                                existing["demand_quantity"]
                            ),
                            "order_count": int(
                                existing["order_count"]
                            ),
                        }
                    )

            current_date += timedelta(days=1)

        result.sort(
            key=lambda row: (
                row["date"],
                str(row["restaurant"]),
                row["item_id"],
            )
        )

        return result