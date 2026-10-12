from __future__ import annotations

from typing import Any


class DemandProfileBuilder:
    """
    Builds a statistical demand profile for each
    restaurant + item combination.

    No forecasting is performed here.
    """

    def __init__(self, calendar: list[dict[str, Any]]):
        self.calendar = calendar

    def build(self) -> list[dict[str, Any]]:
        grouped: dict[tuple[Any, Any], dict[str, Any]] = {}

        for row in self.calendar:
            restaurant = row.get("restaurant")
            item_id = row.get("item_id")

            if item_id is None:
                continue

            key = (restaurant, item_id)

            if key not in grouped:
                grouped[key] = {
                    "restaurant": restaurant,
                    "item_id": item_id,
                    "item_name": row.get("item_name"),
                    "calendar_days": 0,
                    "active_days": 0,
                    "zero_demand_days": 0,
                    "total_demand": 0.0,
                    "max_daily_demand": 0.0,
                }

            profile = grouped[key]

            quantity = float(
                row.get("demand_quantity", 0.0)
            )

            profile["calendar_days"] += 1
            profile["total_demand"] += quantity

            if quantity > 0:
                profile["active_days"] += 1

            if quantity == 0:
                profile["zero_demand_days"] += 1

            profile["max_daily_demand"] = max(
                profile["max_daily_demand"],
                quantity,
            )

        result: list[dict[str, Any]] = []

        for profile in grouped.values():
            calendar_days = profile["calendar_days"]
            active_days = profile["active_days"]
            total_demand = profile["total_demand"]

            average_daily_demand = (
                total_demand / calendar_days
                if calendar_days
                else 0.0
            )

            average_active_demand = (
                total_demand / active_days
                if active_days
                else 0.0
            )

            demand_frequency = (
                active_days / calendar_days
                if calendar_days
                else 0.0
            )

            zero_demand_ratio = (
                profile["zero_demand_days"] / calendar_days
                if calendar_days
                else 0.0
            )

            result.append(
                {
                    "restaurant": profile["restaurant"],
                    "item_id": profile["item_id"],
                    "item_name": profile["item_name"],
                    "calendar_days": calendar_days,
                    "active_days": active_days,
                    "zero_demand_days": profile[
                        "zero_demand_days"
                    ],
                    "total_demand": total_demand,
                    "average_daily_demand": average_daily_demand,
                    "average_active_demand": average_active_demand,
                    "max_daily_demand": profile[
                        "max_daily_demand"
                    ],
                    "demand_frequency": demand_frequency,
                    "zero_demand_ratio": zero_demand_ratio,
                }
            )

        result.sort(
            key=lambda row: (
                str(row["restaurant"]),
                row["item_id"],
            )
        )

        return result