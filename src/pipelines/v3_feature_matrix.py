import json
from pathlib import Path

from src.forecasting.feature_matrix import (
    FeatureMatrixBuilder,
)


INPUT_PATH = Path(
    "data/features/forecast_dataset.json"
)

OUTPUT_PATH = Path(
    "data/features/feature_matrix.json"
)

REPORT_PATH = Path(
    "data/reports/feature_matrix.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 23 - FEATURE MATRIX")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )

    rows = payload["rows"]

    matrix = FeatureMatrixBuilder(rows).build()

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
                "rows": matrix.rows,
                "feature_columns": matrix.feature_columns,
                "target_column": matrix.target_column,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 23",
        "description": "Forecast feature matrix",
        "input_rows": len(rows),
        "output_rows": len(matrix.rows),
        "excluded_rows": matrix.excluded_rows,
        "feature_count": len(matrix.feature_columns),
        "feature_columns": matrix.feature_columns,
        "target_column": matrix.target_column,
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Input rows:             {len(rows):,}")
    print(f"Output rows:            {len(matrix.rows):,}")
    print(
        f"Feature count:          "
        f"{len(matrix.feature_columns)}"
    )
    print(
        f"Target column:          "
        f"{matrix.target_column}"
    )

    print()
    print("STATUS: PASSED")

    print(
        f"Excluded rows:         "
        f"{matrix.excluded_rows:,}"
    )


if __name__ == "__main__":
    main()