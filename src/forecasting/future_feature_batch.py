from __future__ import annotations

from dataclasses import dataclass

from src.forecasting.future_feature_matrix import (
    FutureFeatureMatrixRow,
)


@dataclass(frozen=True)
class FutureFeatureBatch:
    rows: list[FutureFeatureMatrixRow]


class FutureFeatureBatchBuilder:
    def build(
        self,
        rows: list[FutureFeatureMatrixRow],
    ) -> FutureFeatureBatch:

        if not rows:
            raise ValueError(
                "Future feature rows must not be empty"
            )

        dates = [row.date for row in rows]

        if len(set(dates)) != len(dates):
            raise ValueError(
                "Future feature dates must be unique"
            )

        identities = {
            (row.restaurant, row.item_id)
            for row in rows
        }

        if len(identities) != 1:
            raise ValueError(
                "All rows must belong to the same "
                "restaurant and item"
            )

        return FutureFeatureBatch(rows=rows)