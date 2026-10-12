from __future__ import annotations

from datetime import date
from typing import Any


class FeatureValidationError(Exception):
    pass


class TimeSeriesFeatureValidator:
    REQUIRED_FIELDS = {
        "date",
        "restaurant",
        "item_id",
        "item_name",
        "demand_quantity",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_mean_28",
        "rolling_max_7",
        "rolling_std_7",
        "day_of_week",
        "day_of_month",
        "month",
        "is_weekend",
    }

    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows
        self.errors: list[str] = []

    def validate_schema(self) -> None:
        for index, row in enumerate(self.rows):
            missing = self.REQUIRED_FIELDS - set(row.keys())

            if missing:
                self.errors.append(
                    f"row {index}: missing fields {sorted(missing)}"
                )

    def validate_identity(self) -> None:
        seen: set[tuple[Any, Any, Any]] = set()

        for row in self.rows:
            key = (
                row.get("date"),
                row.get("restaurant"),
                row.get("item_id"),
            )

            if key in seen:
                self.errors.append(
                    f"duplicate time-series key: {key}"
                )

            seen.add(key)

    def validate_dates(self) -> None:
        for row in self.rows:
            value = row.get("date")

            try:
                date.fromisoformat(str(value))
            except ValueError:
                self.errors.append(
                    f"invalid date: {value}"
                )

    def validate_demand(self) -> None:
        for row in self.rows:
            quantity = row.get("demand_quantity")

            if not isinstance(quantity, (int, float)):
                self.errors.append(
                    f"non-numeric demand: {quantity}"
                )
                continue

            if quantity < 0:
                self.errors.append(
                    f"negative demand: {quantity}"
                )

    def validate_calendar_features(self) -> None:
        for row in self.rows:
            day_of_week = row.get("day_of_week")
            day_of_month = row.get("day_of_month")
            month = row.get("month")
            is_weekend = row.get("is_weekend")

            if not 0 <= day_of_week <= 6:
                self.errors.append(
                    f"invalid day_of_week: {day_of_week}"
                )

            if not 1 <= day_of_month <= 31:
                self.errors.append(
                    f"invalid day_of_month: {day_of_month}"
                )

            if not 1 <= month <= 12:
                self.errors.append(
                    f"invalid month: {month}"
                )

            if is_weekend not in (0, 1):
                self.errors.append(
                    f"invalid is_weekend: {is_weekend}"
                )

    def validate_lag_values(self) -> None:
        groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]]
        ] = {}

        for row in self.rows:
            key = (
                row.get("restaurant"),
                row.get("item_id"),
            )

            groups.setdefault(key, []).append(row)

        for key, rows in groups.items():
            rows.sort(
                key=lambda row: row["date"]
            )

            values = [
                float(row["demand_quantity"])
                for row in rows
            ]

            for index, row in enumerate(rows):
                expected_lags = {
                    "lag_1": 1,
                    "lag_7": 7,
                    "lag_14": 14,
                    "lag_28": 28,
                }

                for field, offset in expected_lags.items():
                    expected_index = index - offset
                    actual = row.get(field)

                    if expected_index < 0:
                        if actual is not None:
                            self.errors.append(
                                f"{key} {row['date']}: "
                                f"{field} should be None"
                            )
                    else:
                        expected = values[expected_index]

                        if actual != expected:
                            self.errors.append(
                                f"{key} {row['date']}: "
                                f"{field}={actual}, "
                                f"expected={expected}"
                            )

    def validate_rolling_features(self) -> None:
        groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]]
        ] = {}

        for row in self.rows:
            key = (
                row.get("restaurant"),
                row.get("item_id"),
            )

            groups.setdefault(key, []).append(row)

        for key, rows in groups.items():
            rows.sort(
                key=lambda row: row["date"]
            )

            values = [
                float(row["demand_quantity"])
                for row in rows
            ]

            for index, row in enumerate(rows):
                history = values[
                    max(0, index - 7):index
                ]

                actual = row.get(
                    "rolling_mean_7"
                )

                if not history:
                    if actual is not None:
                        self.errors.append(
                            f"{key} {row['date']}: "
                            "rolling_mean_7 should be None"
                        )
                    continue

                expected = sum(history) / len(history)

                if actual != expected:
                    self.errors.append(
                        f"{key} {row['date']}: "
                        f"rolling_mean_7={actual}, "
                        f"expected={expected}"
                    )

                # The current target must never be
                # included in the rolling history.
                

    def validate(self) -> list[str]:
        self.errors = []

        self.validate_schema()
        self.validate_identity()
        self.validate_dates()
        self.validate_demand()
        self.validate_calendar_features()
        self.validate_lag_values()
        self.validate_rolling_features()

        return self.errors

    def is_valid(self) -> bool:
        return not self.errors