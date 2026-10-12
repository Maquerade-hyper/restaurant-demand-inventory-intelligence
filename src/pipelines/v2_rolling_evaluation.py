import json
from pathlib import Path

from src.forecasting.rolling_aggregation import (
    aggregate_rolling_results,
)
from src.forecasting.rolling_evaluator import (
    RollingEvaluator,
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
        "V2 PART 22 - ROLLING EVALUATION"
    )
    print("=" * 70)

    rows = load_time_series_features()

    evaluator = RollingEvaluator(
        rows,
        test_days=14,
        windows=3,
    )

    rolling_results = evaluator.evaluate()

    print(
        f"Input rows:             "
        f"{len(rows):,}"
    )

    print(
        f"Rolling windows:        "
        f"{len(rolling_results):,}"
    )

    print()

    for result in rolling_results:
        print(
            f"Window {result['window']}: "
            f"cutoff={result['cutoff_date']} "
            f"train={result['train_rows']:,} "
            f"test={result['test_rows']:,}"
        )

    print()

    aggregated = aggregate_rolling_results(
        rolling_results
    )

    current_segment = None

    for row in aggregated:
        if row["segment"] != current_segment:
            current_segment = row["segment"]

            print(
                f"[{current_segment}]"
            )

        print(
            f"  {row['model']:<20}"
            f" windows={row['windows']}"
            f" MAE={row['mae_mean']:.6f}"
            f" RMSE={row['rmse_mean']:.6f}"
            f" sMAPE={row['smape_mean']:.6f}%"
        )

    print()

    output_path = Path(
        "data/features/"
        "rolling_evaluation.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            rolling_results,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V2 Part 22",
        "description": (
            "Rolling-origin model evaluation"
        ),
        "input_rows": len(rows),
        "windows": len(rolling_results),
        "test_days": 14,
        "aggregated_results": aggregated,
    }

    report_path = Path(
        "data/reports/"
        "rolling_evaluation.json"
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