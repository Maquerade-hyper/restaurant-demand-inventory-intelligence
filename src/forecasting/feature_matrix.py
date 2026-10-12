from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FeatureMatrix:
    rows: list[dict[str, Any]]
    feature_columns: list[str]
    target_column: str
    excluded_rows: int


class FeatureMatrixBuilder:
    TARGET_COLUMN = "demand_quantity"

    FEATURE_COLUMNS = [
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
    ]

    ID_COLUMNS = [
        "date",
        "restaurant",
        "item_id",
    ]

    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def build(self) -> FeatureMatrix:
        matrix: list[dict[str, Any]] = []
        excluded_rows = 0

        required = (
            self.ID_COLUMNS
            + self.FEATURE_COLUMNS
            + [self.TARGET_COLUMN]
        )

        for index, row in enumerate(self.rows):
            missing = [
                column
                for column in required
                if column not in row
            ]

            if missing:
                raise ValueError(
                    f"Row {index} missing columns: {missing}"
                )

            # Historical features can legitimately be unavailable
            # at the beginning of a time series.
            unavailable = [
                column
                for column in self.FEATURE_COLUMNS
                if row[column] is None
            ]

            if unavailable:
                excluded_rows += 1
                continue

            record: dict[str, Any] = {}

            for column in self.ID_COLUMNS:
                record[column] = row[column]

            for column in self.FEATURE_COLUMNS:
                record[column] = float(row[column])

            target = row[self.TARGET_COLUMN]

            if target is None:
                raise ValueError(
                    f"Null target at row {index}"
                )

            target = float(target)

            if target < 0:
                raise ValueError(
                    f"Negative target at row {index}"
                )

            record[self.TARGET_COLUMN] = target

            matrix.append(record)

        return FeatureMatrix(
            rows=matrix,
            feature_columns=list(self.FEATURE_COLUMNS),
            target_column=self.TARGET_COLUMN,
            excluded_rows=excluded_rows,
        )