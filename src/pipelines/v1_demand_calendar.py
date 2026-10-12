from __future__ import annotations

import json
from pathlib import Path

from src.features.demand_calendar import DemandCalendarBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "daily_demand.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "demand_calendar.json"
)


def main() -> None:
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        daily_demand = json.load(file)

    builder = DemandCalendarBuilder(daily_demand)

    calendar = builder.build()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            calendar,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 DEMAND CALENDAR")
    print("=" * 70)

    print(f"Daily demand rows:      {len(daily_demand)}")
    print(f"Calendar rows:          {len(calendar)}")
    print(f"Output:                 {OUTPUT_FILE}")

    if not calendar:
        raise RuntimeError(
            "Demand calendar is empty"
        )

    dates = {
        row["date"]
        for row in calendar
    }

    combinations = {
        (
            row["restaurant"],
            row["item_id"],
        )
        for row in calendar
    }

    zero_demand_rows = sum(
        1
        for row in calendar
        if row["demand_quantity"] == 0
    )

    positive_demand_rows = sum(
        1
        for row in calendar
        if row["demand_quantity"] > 0
    )

    print(f"Calendar dates:         {len(dates)}")
    print(f"Item/restaurant pairs:  {len(combinations)}")
    print(f"Zero-demand rows:       {zero_demand_rows}")
    print(f"Positive-demand rows:   {positive_demand_rows}")

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()