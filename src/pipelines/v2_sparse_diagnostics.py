import json
from pathlib import Path

from src.forecasting.sparse_diagnostics import (
    build_sparse_diagnostics,
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
        "V2 PART 16 - SPARSE-DEMAND DIAGNOSTICS"
    )
    print("=" * 70)

    rows = load_time_series_features()

    diagnostics = build_sparse_diagnostics(
        rows
    )

    print(
        f"Input rows:             "
        f"{len(rows):,}"
    )

    print(
        f"Demand series:          "
        f"{len(diagnostics):,}"
    )

    total_days = sum(
        row["total_days"]
        for row in diagnostics
    )

    total_active_days = sum(
        row["active_days"]
        for row in diagnostics
    )

    total_zero_days = sum(
        row["zero_days"]
        for row in diagnostics
    )

    total_demand = sum(
        row["total_demand"]
        for row in diagnostics
    )

    print(
        f"Total series-days:      "
        f"{total_days:,}"
    )

    print(
        f"Active series-days:     "
        f"{total_active_days:,}"
    )

    print(
        f"Zero series-days:       "
        f"{total_zero_days:,}"
    )

    print(
        f"Total demand:           "
        f"{total_demand:.3f}"
    )

    overall_frequency = (
        total_active_days / total_days
        if total_days
        else 0.0
    )

    print(
        f"Overall demand freq.:   "
        f"{overall_frequency:.6f}"
    )

    print()

    output_path = Path(
        "data/features/sparse_diagnostics.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            diagnostics,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V2 Part 16",
        "description": (
            "Sparse-demand diagnostics"
        ),
        "input_rows": len(rows),
        "demand_series": len(diagnostics),
        "total_series_days": total_days,
        "active_series_days": total_active_days,
        "zero_series_days": total_zero_days,
        "total_demand": total_demand,
        "overall_demand_frequency": (
            overall_frequency
        ),
    }

    report_path = Path(
        "data/reports/sparse_diagnostics.json"
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