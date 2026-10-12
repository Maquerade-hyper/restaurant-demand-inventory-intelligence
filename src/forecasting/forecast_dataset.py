from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ForecastDataset:
    rows: list[dict[str, Any]]
    feature_columns: list[str]
    target_column: str


class ForecastDatasetBuilder:
    """
    Builds the model-ready forecasting dataset.

    Input:
        data/features/time_series_features.json

    Output:
        Rows containing:
        - identity columns
        - target
        - leakage-safe historical features
        - calendar features

    No random sampling.
    No target leakage.
    No business-rule inference.
    """

    TARGET_COLUMN = "demand_quantity"

    ID_COLUMNS = [
        "date",
        "restaurant",
        "item_id",
    ]

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

    REQUIRED_COLUMNS = (
        ID_COLUMNS
        + [TARGET_COLUMN]
        + FEATURE_COLUMNS
    )

    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def build(self) -> ForecastDataset:
        if not isinstance(self.rows, list):
            raise TypeError("rows must be a list")

        output: list[dict[str, Any]] = []

        for index, row in enumerate(self.rows):
            if not isinstance(row, dict):
                raise TypeError(
                    f"Row {index} must be a dictionary"
                )

            missing = [
                column
                for column in self.REQUIRED_COLUMNS
                if column not in row
            ]

            if missing:
                raise ValueError(
                    f"Row {index} missing columns: {missing}"
                )

            record = {
                column: row[column]
                for column in self.REQUIRED_COLUMNS
            }

            output.append(record)

        return ForecastDataset(
            rows=output,
            feature_columns=list(self.FEATURE_COLUMNS),
            target_column=self.TARGET_COLUMN,
        )