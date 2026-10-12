from __future__ import annotations

import json
from pathlib import Path

from src.validation.feature_validation import (
    TimeSeriesFeatureValidator,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
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
        rows = json.load(file)

    validator = TimeSeriesFeatureValidator(rows)

    errors = validator.validate()

    print("=" * 70)
    print(
        "RESTAURANT DEMAND & INVENTORY INTELLIGENCE"
    )
    print("V1 FEATURE VALIDATION")
    print("=" * 70)

    print(f"Rows checked:           {len(rows)}")
    print(f"Validation errors:      {len(errors)}")

    if errors:
        print()

        for error in errors[:20]:
            print(f"[ERROR] {error}")

        if len(errors) > 20:
            print(
                f"... and {len(errors) - 20} more"
            )

        raise RuntimeError(
            "Feature validation failed"
        )

    print()
    print("Schema:                 PASSED")
    print("Identity:               PASSED")
    print("Dates:                  PASSED")
    print("Demand:                 PASSED")
    print("Calendar features:      PASSED")
    print("Lag features:           PASSED")
    print("Rolling features:       PASSED")
    print()
    print("V1 STATUS: PASSED")


if __name__ == "__main__":
    main()