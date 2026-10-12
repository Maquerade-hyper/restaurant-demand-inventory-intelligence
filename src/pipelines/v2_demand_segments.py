import json
from collections import Counter
from pathlib import Path

from src.forecasting.demand_segments import (
    build_demand_segments,
)


def load_time_series_features() -> list[dict]:
    path = Path(
        "data/features/time_series_features.json"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Feature file not found: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def main() -> None:
    print("=" * 70)
    print(
        "RESTAURANT DEMAND & INVENTORY INTELLIGENCE"
    )
    print(
        "V2 PART 15 - DEMAND-ACTIVITY SEGMENTATION"
    )
    print("=" * 70)

    rows = load_time_series_features()

    segments = build_demand_segments(rows)

    counts = Counter(
        segment["classification"]
        for segment in segments
    )

    print(
        f"Input rows:             "
        f"{len(rows):,}"
    )

    print(
        f"Demand series:          "
        f"{len(segments):,}"
    )

    print()

    for classification in (
        "frequent",
        "intermittent",
        "sparse",
        "no_demand",
    ):
        print(
            f"{classification:<20}"
            f"{counts.get(classification, 0):,}"
        )

    print()

    output_path = Path(
        "data/features/demand_segments.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            segments,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V2 Part 15",
        "description": (
            "Demand-activity segmentation"
        ),
        "input_rows": len(rows),
        "series": len(segments),
        "classification_counts": dict(counts),
    }

    report_path = Path(
        "data/reports/demand_segments.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Feature output:        "
        f"{output_path.resolve()}"
    )

    print(
        f"Report:                 "
        f"{report_path.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()