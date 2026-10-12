from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ForecastTarget:
    values: list[float]
    positive_count: int
    zero_count: int
    total_demand: float


class ForecastTargetBuilder:
    TARGET_COLUMN = "demand_quantity"

    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def build(self) -> ForecastTarget:
        values: list[float] = []

        for index, row in enumerate(self.rows):
            if self.TARGET_COLUMN not in row:
                raise ValueError(
                    f"Row {index} missing target column: "
                    f"{self.TARGET_COLUMN}"
                )

            value = float(row[self.TARGET_COLUMN])

            if value < 0:
                raise ValueError(
                    f"Negative demand at row {index}: {value}"
                )

            values.append(value)

        positive_count = sum(
            1 for value in values if value > 0
        )

        zero_count = sum(
            1 for value in values if value == 0
        )

        total_demand = sum(values)

        return ForecastTarget(
            values=values,
            positive_count=positive_count,
            zero_count=zero_count,
            total_demand=total_demand,
        )