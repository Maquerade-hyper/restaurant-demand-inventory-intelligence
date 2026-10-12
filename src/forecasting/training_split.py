from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TrainingSplit:
    train: list[dict[str, Any]]
    validation: list[dict[str, Any]]
    cutoff_date: str


class ChronologicalTrainingSplitter:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        validation_days: int = 14,
    ):
        if validation_days <= 0:
            raise ValueError(
                "validation_days must be greater than 0"
            )

        self.rows = rows
        self.validation_days = validation_days

    def split(self) -> TrainingSplit:
        if not self.rows:
            raise ValueError("rows cannot be empty")

        dates = sorted(
            {str(row["date"]) for row in self.rows}
        )

        if len(dates) <= self.validation_days:
            raise ValueError(
                "Not enough dates for chronological split"
            )

        cutoff_index = (
            len(dates) - self.validation_days
        )

        cutoff_date = dates[cutoff_index]

        train = [
            row
            for row in self.rows
            if str(row["date"]) < cutoff_date
        ]

        validation = [
            row
            for row in self.rows
            if str(row["date"]) >= cutoff_date
        ]

        if not train:
            raise ValueError(
                "Training dataset cannot be empty"
            )

        if not validation:
            raise ValueError(
                "Validation dataset cannot be empty"
            )

        return TrainingSplit(
            train=train,
            validation=validation,
            cutoff_date=cutoff_date,
        )