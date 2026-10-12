import json
from pathlib import Path

from src.forecasting.forecast_dataset import ForecastDatasetBuilder


INPUT_PATH = Path("data/features/time_series_features.json")
OUTPUT_PATH = Path("data/features/forecast_dataset.json")
REPORT_PATH = Path("data/reports/forecast_dataset.json")


def load_input() -> list[dict]:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    return json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 21 - FORECAST DATASET")
    print("=" * 70)

    rows = load_input()

    builder = ForecastDatasetBuilder(rows)
    dataset = builder.build()

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
                "rows": dataset.rows,
                "feature_columns": dataset.feature_columns,
                "target_column": dataset.target_column,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 21",
        "description": "Model-ready forecast dataset",
        "input_rows": len(rows),
        "output_rows": len(dataset.rows),
        "target_column": dataset.target_column,
        "feature_columns": dataset.feature_columns,
        "identity_columns": ForecastDatasetBuilder.ID_COLUMNS,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Input rows:             {len(rows):,}")
    print(f"Output rows:            {len(dataset.rows):,}")
    print(
        f"Feature columns:        "
        f"{len(dataset.feature_columns)}"
    )
    print(
        f"Target column:          "
        f"{dataset.target_column}"
    )

    print()
    print("Feature columns:")
    for column in dataset.feature_columns:
        print(f"  - {column}")

    print()
    print(f"Feature output:        {OUTPUT_PATH.resolve()}")
    print(f"Report:                {REPORT_PATH.resolve()}")
    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()