from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RollingWindow:
    train: list[dict[str, Any]]
    test: list[dict[str, Any]]
    cutoff_date: str


class RollingBacktester:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        test_days: int = 14,
        windows: int = 3,
    ) -> None:
        if test_days <= 0:
            raise ValueError(
                "test_days must be greater than zero"
            )

        if windows <= 0:
            raise ValueError(
                "windows must be greater than zero"
            )

        self.rows = rows
        self.test_days = test_days
        self.windows = windows

    def split(self) -> list[RollingWindow]:
        dates = sorted(
            {
                str(row["date"])
                for row in self.rows
            }
        )

        if len(dates) <= self.test_days:
            return []

        max_start = (
            len(dates) - self.test_days
        )

        first_start = max(
            1,
            max_start - self.windows,
        )

        windows: list[RollingWindow] = []

        for test_start in range(
            first_start,
            max_start,
        ):
            test_dates = dates[
                test_start:
                test_start + self.test_days
            ]

            if len(test_dates) != self.test_days:
                continue

            cutoff_date = test_dates[0]

            train = [
                row
                for row in self.rows
                if str(row["date"]) < cutoff_date
            ]

            test = [
                row
                for row in self.rows
                if str(row["date"]) in test_dates
            ]

            windows.append(
                RollingWindow(
                    train=train,
                    test=test,
                    cutoff_date=cutoff_date,
                )
            )

        return windows