import json
from pathlib import Path

from src.forecasting.target_preparation import (
    ForecastTargetBuilder,
)


INPUT_PATH = Path(
    "data/features/forecast_dataset.json"
)

OUTPUT_PATH = Path(
    "data/features/forecast_target.json"
)

REPORT_PATH = Path(
    "data/reports/forecast_target.json"
)


def load_input() -> list[dict]:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )

    return payload["rows"]


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 22 - FORECAST TARGET PREPARATION")
    print("=" * 70)

    rows = load_input()

    builder = ForecastTargetBuilder(rows)
    target = builder.build()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "target_column": (
                    ForecastTargetBuilder.TARGET_COLUMN
                ),
                "values": target.values,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 22",
        "description": "Forecast target preparation",
        "input_rows": len(rows),
        "target_column": (
            ForecastTargetBuilder.TARGET_COLUMN
        ),
        "positive_count": target.positive_count,
        "zero_count": target.zero_count,
        "total_demand": target.total_demand,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Input rows:             {len(rows):,}")
    print(
        f"Positive targets:      "
        f"{target.positive_count:,}"
    )
    print(
        f"Zero targets:          "
        f"{target.zero_count:,}"
    )
    print(
        f"Total demand:          "
        f"{target.total_demand:.3f}"
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