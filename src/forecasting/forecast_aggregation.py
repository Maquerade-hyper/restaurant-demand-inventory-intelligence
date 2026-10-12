from __future__ import annotations

from collections import defaultdict
from typing import Any


class ForecastAggregator:

    def by_item_restaurant(
        self,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        grouped: dict[tuple[str, int], dict[str, float]] = (
            defaultdict(
                lambda: {
                    "actual": 0.0,
                    "predicted": 0.0,
                }
            )
        )

        for row in rows:
            key = (
                str(row["restaurant"]),
                int(row["item_id"]),
            )

            grouped[key]["actual"] += float(
                row["actual"]
            )
            grouped[key]["predicted"] += float(
                row["predicted"]
            )

        output = []

        for (restaurant, item_id), values in sorted(
            grouped.items()
        ):
            output.append(
                {
                    "restaurant": restaurant,
                    "item_id": item_id,
                    "actual": values["actual"],
                    "predicted": values["predicted"],
                }
            )

        return output

    def by_restaurant(
        self,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, float]] = (
            defaultdict(
                lambda: {
                    "actual": 0.0,
                    "predicted": 0.0,
                }
            )
        )

        for row in rows:
            restaurant = str(
                row["restaurant"]
            )

            grouped[restaurant]["actual"] += float(
                row["actual"]
            )

            grouped[restaurant]["predicted"] += float(
                row["predicted"]
            )

        return [
            {
                "restaurant": restaurant,
                "actual": values["actual"],
                "predicted": values["predicted"],
            }
            for restaurant, values in sorted(
                grouped.items()
            )
        ]

    def overall(
        self,
        rows: list[dict[str, Any]],
    ) -> dict[str, float]:
        actual = sum(
            float(row["actual"])
            for row in rows
        )

        predicted = sum(
            float(row["predicted"])
            for row in rows
        )

        return {
            "actual": actual,
            "predicted": predicted,
        }