from __future__ import annotations

import json
from pathlib import Path

from src.features.demand_profile import DemandProfileBuilder


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
    / "demand_profile.json"
)


def main() -> None:
    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        calendar = json.load(file)

    builder = DemandProfileBuilder(calendar)

    profiles = builder.build()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            profiles,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 DEMAND PROFILE")
    print("=" * 70)

    print(f"Calendar rows:          {len(calendar)}")
    print(f"Demand profiles:        {len(profiles)}")
    print(f"Output:                 {OUTPUT_FILE}")

    if not profiles:
        raise RuntimeError(
            "Demand profile is empty"
        )

    total_active_days = sum(
        row["active_days"]
        for row in profiles
    )

    total_zero_days = sum(
        row["zero_demand_days"]
        for row in profiles
    )

    total_demand = sum(
        row["total_demand"]
        for row in profiles
    )

    max_daily_demand = max(
        row["max_daily_demand"]
        for row in profiles
    )

    print(f"Total active days:      {total_active_days}")
    print(f"Total zero-demand days: {total_zero_days}")
    print(f"Total demand:           {total_demand}")
    print(f"Maximum daily demand:   {max_daily_demand}")

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()