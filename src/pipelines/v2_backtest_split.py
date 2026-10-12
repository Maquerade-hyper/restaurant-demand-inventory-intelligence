from __future__ import annotations

import json
from pathlib import Path

from src.forecasting.backtest_split import (
    ChronologicalBacktester,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "demand_calendar.json"
)

TEST_DAYS = 14


def main() -> None:
    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        rows = json.load(file)

    backtester = ChronologicalBacktester(
        rows,
        test_days=TEST_DAYS,
    )

    split = backtester.split()

    print("=" * 70)
    print(
        "RESTAURANT DEMAND & INVENTORY INTELLIGENCE"
    )
    print("V2 PART 11 - BACKTEST SPLIT")
    print("=" * 70)

    print(f"Total rows:             {len(rows)}")
    print(f"Train rows:             {len(split.train)}")
    print(f"Test rows:              {len(split.test)}")
    print(f"Test days:              {TEST_DAYS}")
    print(f"Cutoff date:            {split.cutoff_date}")

    if not split.train:
        raise RuntimeError(
            "Training set is empty"
        )

    if not split.test:
        raise RuntimeError(
            "Test set is empty"
        )

    train_dates = {
        row["date"]
        for row in split.train
    }

    test_dates = {
        row["date"]
        for row in split.test
    }

    if train_dates & test_dates:
        raise RuntimeError(
            "Temporal leakage: train/test dates overlap"
        )

    print()
    print("Chronological separation: PASSED")
    print("Temporal leakage check:   PASSED")
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()