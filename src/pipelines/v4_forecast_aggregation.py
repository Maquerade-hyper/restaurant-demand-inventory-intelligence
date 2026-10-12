import json
from pathlib import Path

from src.forecasting.forecast_aggregation import (
    ForecastAggregator,
)


INPUT_PATH = Path(
    "data/features/forecast_results.json"
)

OUTPUT_PATH = Path(
    "data/features/forecast_aggregation.json"
)

REPORT_PATH = Path(
    "data/reports/forecast_aggregation.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 36 - FORECAST AGGREGATION")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(
            encoding="utf-8"
        )
    )

    rows = payload["results"]

    aggregator = ForecastAggregator()

    item_restaurant = (
        aggregator.by_item_restaurant(rows)
    )

    restaurants = aggregator.by_restaurant(
        rows
    )

    overall = aggregator.overall(rows)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "item_restaurant": item_restaurant,
        "restaurant": restaurants,
        "overall": overall,
    }

    OUTPUT_PATH.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V4 Part 36",
        "description": (
            "Forecast aggregation"
        ),
        "input_rows": len(rows),
        "item_restaurant_groups": len(
            item_restaurant
        ),
        "restaurant_groups": len(
            restaurants
        ),
        "overall": overall,
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print(
        f"Input forecast rows:   "
        f"{len(rows):,}"
    )

    print(
        f"Item/restaurant:       "
        f"{len(item_restaurant):,}"
    )

    print(
        f"Restaurants:            "
        f"{len(restaurants):,}"
    )

    print()
    print("Overall:")
    print(
        f"  actual={overall['actual']:.6f}"
    )
    print(
        f"  predicted={overall['predicted']:.6f}"
    )

    print()
    print(
        f"Feature output:        "
        f"{OUTPUT_PATH.resolve()}"
    )

    print(
        f"Report:                "
        f"{REPORT_PATH.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()