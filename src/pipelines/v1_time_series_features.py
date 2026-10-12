from __future__ import annotations

import json
from pathlib import Path

from src.features.time_series_features import (
    TimeSeriesFeatureBuilder,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "demand_calendar.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "time_series_features.json"
)


def main() -> None:
    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        calendar = json.load(file)

    builder = TimeSeriesFeatureBuilder(
        calendar
    )

    features = builder.build()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            features,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print(
        "RESTAURANT DEMAND & INVENTORY INTELLIGENCE"
    )
    print("V1 TIME-SERIES FEATURES")
    print("=" * 70)

    print(
        f"Calendar rows:          {len(calendar)}"
    )

    print(
        f"Feature rows:           {len(features)}"
    )

    print(
        f"Output:                 {OUTPUT_FILE}"
    )

    if not features:
        raise RuntimeError(
            "Time-series feature dataset is empty"
        )

    complete_lag_28 = sum(
        1
        for row in features
        if row["lag_28"] is not None
    )

    positive_targets = sum(
        1
        for row in features
        if row["demand_quantity"] > 0
    )

    zero_targets = sum(
        1
        for row in features
        if row["demand_quantity"] == 0
    )

    print(
        f"Rows with lag_28:       "
        f"{complete_lag_28}"
    )

    print(
        f"Positive targets:       "
        f"{positive_targets}"
    )

    print(
        f"Zero targets:           "
        f"{zero_targets}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()