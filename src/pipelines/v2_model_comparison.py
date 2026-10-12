import json
from pathlib import Path

from src.forecasting.backtest_split import (
    ChronologicalBacktester,
)
from src.forecasting.baseline_evaluator import (
    BaselineEvaluator,
)
from src.forecasting.intermittent_evaluator import (
    IntermittentBaselineEvaluator,
)
from src.forecasting.model_comparison import (
    build_model_comparison,
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
        "V2 PART 19 - BASELINE MODEL COMPARISON"
    )
    print("=" * 70)

    rows = load_time_series_features()

    backtester = ChronologicalBacktester(
        rows,
        test_days=14,
    )

    split = backtester.split()

    test_dates = {
        row["date"]
        for row in split.test
    }

    print(
        f"Train rows:             "
        f"{len(split.train):,}"
    )

    print(
        f"Test rows:              "
        f"{len(split.test):,}"
    )

    print(
        f"Test days:              "
        f"{len(test_dates):,}"
    )

    print()

    baseline_evaluator = BaselineEvaluator(
        split.train,
        split.test,
    )

    intermittent_evaluator = (
        IntermittentBaselineEvaluator(
            split.train,
            split.test,
        )
    )

    baseline_results = (
        baseline_evaluator.evaluate_segments()
    )

    intermittent_results = (
        intermittent_evaluator.evaluate()
    )

    comparison = build_model_comparison(
        baseline_results,
        intermittent_results,
    )

    current_segment = None

    for row in comparison:
        if row["segment"] != current_segment:
            current_segment = row["segment"]

            print(
                f"[{current_segment}]"
            )

        print(
            f"  {row['model']:<20}"
            f" MAE={row['mae']:.6f}"
            f"  RMSE={row['rmse']:.6f}"
            f"  sMAPE={row['smape']:.6f}%"
        )

    print()

    report = {
        "part": "V2 Part 19",
        "description": (
            "Baseline model comparison"
        ),
        "train_rows": len(split.train),
        "test_rows": len(split.test),
        "test_days": len(test_dates),
        "cutoff_date": split.cutoff_date,
        "models": [
            "naive",
            "seasonal_naive_7",
            "moving_average_7",
            "croston",
            "sba_croston",
        ],
        "segments": [
            "all",
            "zero_actual",
            "positive_actual",
        ],
        "comparison": comparison,
    }

    output_path = Path(
        "data/features/model_comparison.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            comparison,
            indent=2,
        ),
        encoding="utf-8",
    )

    report_path = Path(
        "data/reports/model_comparison.json"
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