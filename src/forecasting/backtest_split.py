from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class BacktestSplit:
    train: list[dict[str, Any]]
    test: list[dict[str, Any]]
    cutoff_date: str


class ChronologicalBacktester:
    """
    Creates chronological train/test splits.

    No random shuffling is allowed.

    For every restaurant + item series:
        train = observations before cutoff
        test  = observations on/after cutoff
    """

    def __init__(
        self,
        rows: list[dict[str, Any]],
        test_days: int,
    ):
        if test_days <= 0:
            raise ValueError(
                "test_days must be greater than zero"
            )

        self.rows = rows
        self.test_days = test_days

    def split(self) -> BacktestSplit:
        if not self.rows:
            raise ValueError(
                "Cannot split an empty dataset"
            )

        dates = sorted(
            {
                date.fromisoformat(
                    str(row["date"])
                )
                for row in self.rows
            }
        )

        if len(dates) <= self.test_days:
            raise ValueError(
                "Not enough dates for requested test window"
            )

        cutoff = dates[-self.test_days]

        train: list[dict[str, Any]] = []
        test: list[dict[str, Any]] = []

        for row in self.rows:
            row_date = date.fromisoformat(
                str(row["date"])
            )

            if row_date < cutoff:
                train.append(row)
            else:
                test.append(row)

        train.sort(
            key=lambda row: (
                row["date"],
                str(row.get("restaurant")),
                row["item_id"],
            )
        )

        test.sort(
            key=lambda row: (
                row["date"],
                str(row.get("restaurant")),
                row["item_id"],
            )
        )

        return BacktestSplit(
            train=train,
            test=test,
            cutoff_date=cutoff.isoformat(),
        )