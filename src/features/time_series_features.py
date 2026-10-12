from __future__ import annotations

from collections import defaultdict
from datetime import date
from math import sqrt
from typing import Any


class TimeSeriesFeatureBuilder:
    """
    Creates historical forecasting features.

    Grain:
        date + restaurant + item_id

    Leakage rule:
        Features for date T may only use information
        available before date T.

    Therefore:
        lag_1 uses T-1
        rolling_mean_7 uses T-1 ... T-7
        etc.
    """

    def __init__(self, calendar: list[dict[str, Any]]):
        self.calendar = calendar

    @staticmethod
    def _mean(values: list[float]) -> float | None:
        if not values:
            return None

        return sum(values) / len(values)

    @staticmethod
    def _std(values: list[float]) -> float | None:
        if not values:
            return None

        mean = sum(values) / len(values)

        variance = sum(
            (value - mean) ** 2
            for value in values
        ) / len(values)

        return sqrt(variance)

    @staticmethod
    def _lag(
        values: list[float],
        index: int,
        lag: int,
    ) -> float | None:
        position = index - lag

        if position < 0:
            return None

        return values[position]

    @staticmethod
    def _historical_window(
        values: list[float],
        index: int,
        window: int,
    ) -> list[float]:
        """
        Returns only historical values.

        For index T:
            end = T
            start = max(0, T-window)

        Current target values[T] is excluded.
        """

        start = max(0, index - window)

        return values[start:index]

    def build(self) -> list[dict[str, Any]]:
        grouped: dict[
            tuple[Any, Any],
            list[dict[str, Any]],
        ] = defaultdict(list)

        for row in self.calendar:
            item_id = row.get("item_id")

            if item_id is None:
                continue

            key = (
                row.get("restaurant"),
                item_id,
            )

            grouped[key].append(row)

        result: list[dict[str, Any]] = []

        for rows in grouped.values():
            rows.sort(
                key=lambda row: row["date"]
            )

            values = [
                float(
                    row.get(
                        "demand_quantity",
                        0.0,
                    )
                )
                for row in rows
            ]

            for index, row in enumerate(rows):
                current_date = date.fromisoformat(
                    row["date"]
                )

                history_7 = self._historical_window(
                    values,
                    index,
                    7,
                )

                history_14 = self._historical_window(
                    values,
                    index,
                    14,
                )

                history_28 = self._historical_window(
                    values,
                    index,
                    28,
                )

                record = {
                    "date": row["date"],
                    "restaurant": row.get(
                        "restaurant"
                    ),
                    "item_id": row.get("item_id"),
                    "item_name": row.get(
                        "item_name"
                    ),

                    # Target
                    "demand_quantity": float(
                        row.get(
                            "demand_quantity",
                            0.0,
                        )
                    ),

                    # Lag features
                    "lag_1": self._lag(
                        values,
                        index,
                        1,
                    ),
                    "lag_7": self._lag(
                        values,
                        index,
                        7,
                    ),
                    "lag_14": self._lag(
                        values,
                        index,
                        14,
                    ),
                    "lag_28": self._lag(
                        values,
                        index,
                        28,
                    ),

                    # Rolling historical features
                    "rolling_mean_7": self._mean(
                        history_7
                    ),
                    "rolling_mean_14": self._mean(
                        history_14
                    ),
                    "rolling_mean_28": self._mean(
                        history_28
                    ),
                    "rolling_max_7": (
                        max(history_7)
                        if history_7
                        else None
                    ),
                    "rolling_std_7": self._std(
                        history_7
                    ),

                    # Calendar features
                    "day_of_week": (
                        current_date.weekday()
                    ),
                    "day_of_month": (
                        current_date.day
                    ),
                    "month": current_date.month,
                    "is_weekend": int(
                        current_date.weekday()
                        >= 5
                    ),
                }

                result.append(record)

        result.sort(
            key=lambda row: (
                row["date"],
                str(row["restaurant"]),
                row["item_id"],
            )
        )

        return result