from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ForecastResult:
    date: str
    restaurant: str
    item_id: int
    actual: float
    predicted: float


class ForecastResultBuilder:
    def build(
        self,
        rows: list[dict[str, Any]],
        predictions: list[float],
    ) -> list[ForecastResult]:
        if len(rows) != len(predictions):
            raise ValueError(
                "Rows and predictions must have "
                "the same length"
            )

        results: list[ForecastResult] = []

        for index, (row, prediction) in enumerate(
            zip(rows, predictions)
        ):
            required = [
                "date",
                "restaurant",
                "item_id",
                "demand_quantity",
            ]

            missing = [
                field
                for field in required
                if field not in row
            ]

            if missing:
                raise ValueError(
                    f"Row {index} missing fields: "
                    f"{missing}"
                )

            predicted = float(prediction)
            actual = float(
                row["demand_quantity"]
            )

            if predicted < 0:
                raise ValueError(
                    f"Negative prediction at row {index}"
                )

            if actual < 0:
                raise ValueError(
                    f"Negative actual at row {index}"
                )

            results.append(
                ForecastResult(
                    date=str(row["date"]),
                    restaurant=str(
                        row["restaurant"]
                    ),
                    item_id=int(row["item_id"]),
                    actual=actual,
                    predicted=predicted,
                )
            )

        return results