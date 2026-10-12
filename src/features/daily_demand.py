from __future__ import annotations

from collections import defaultdict
from typing import Any


class DailyDemandBuilder:
    """
    Aggregates order-item records into daily demand.

    Grain:
        one row per date + restaurant + item_id

    Rules:
    - item_id remains the primary identity.
    - item_name is descriptive only.
    - quantities are summed.
    - order count is counted.
    - records without item_id are preserved separately
      rather than being merged by name.
    """

    def __init__(self, records: list[dict[str, Any]]):
        self.records = records

    def build(self) -> list[dict[str, Any]]:
        grouped: dict[tuple[Any, Any, Any], dict[str, Any]] = {}

        for record in self.records:
            item_id = record.get("item_id")
            date = record.get("order_date")
            restaurant = record.get("restaurant")

            if item_id is None or date is None:
                continue

            key = (date, restaurant, item_id)

            if key not in grouped:
                grouped[key] = {
                    "date": date,
                    "restaurant": restaurant,
                    "item_id": item_id,
                    "item_name": record.get("item_name"),
                    "demand_quantity": 0.0,
                    "order_count": 0,
                }

            grouped[key]["demand_quantity"] += float(
                record["quantity"]
            )

            grouped[key]["order_count"] += 1

        result = list(grouped.values())

        result.sort(
            key=lambda row: (
                row["date"],
                str(row["restaurant"]),
                row["item_id"],
            )
        )

        return result