from __future__ import annotations

import json
from pathlib import Path

from src.features.daily_demand import DailyDemandBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "order_items.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "daily_demand.json"
)


def main() -> None:
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        order_items = json.load(file)

    builder = DailyDemandBuilder(order_items)

    daily_demand = builder.build()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            daily_demand,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 DAILY DEMAND")
    print("=" * 70)

    print(f"Order-item rows:        {len(order_items)}")
    print(f"Daily demand rows:      {len(daily_demand)}")
    print(f"Output:                 {OUTPUT_FILE}")

    if not daily_demand:
        raise RuntimeError(
            "Daily demand dataset is empty"
        )

    total_demand = sum(
        row["demand_quantity"]
        for row in daily_demand
    )

    unique_items = {
        row["item_id"]
        for row in daily_demand
    }

    unique_days = {
        row["date"]
        for row in daily_demand
    }

    print(f"Unique items:           {len(unique_items)}")
    print(f"Unique dates:           {len(unique_days)}")
    print(f"Total demand quantity:  {total_demand}")

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()