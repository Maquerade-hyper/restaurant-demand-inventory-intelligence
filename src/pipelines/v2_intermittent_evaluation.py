import json
from pathlib import Path

from src.forecasting.backtest_split import (
    ChronologicalBacktester,
)
from src.forecasting.intermittent_evaluator import (
    IntermittentBaselineEvaluator,
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
        "V2 PART 18 - INTERMITTENT BASELINE EVALUATION"
    )
    print("=" * 70)

    rows = load_time_series_features()

    backtester = ChronologicalBacktester(
        rows,
        test_days=14,
    )

    split = backtester.split()

    print(
        f"Train rows:             "
        f"{len(split.train):,}"
    )

    print(
        f"Test rows:              "
        f"{len(split.test):,}"
    )

    test_dates = {
        row["date"]
        for row in split.test
    }

    print(
        f"Test days:              "
        f"{len(test_dates):,}"
    )

    print()

    evaluator = IntermittentBaselineEvaluator(
        split.train,
        split.test,
    )

    results = evaluator.evaluate()

    for model_name, segments in results.items():
        print(f"[{model_name}]")

        for segment_name, metrics in segments.items():
            print(
                f"  [{segment_name}]"
            )

            print(
                f"    MAE:              "
                f"{metrics['mae']:.6f}"
            )

            print(
                f"    RMSE:             "
                f"{metrics['rmse']:.6f}"
            )

            print(
                f"    sMAPE:            "
                f"{metrics['smape']:.6f}%"
            )

        print()

    report = {
        "part": "V2 Part 18",
        "description": (
            "Intermittent baseline evaluation"
        ),
        "train_rows": len(split.train),
        "test_rows": len(split.test),
        "test_days": len(test_dates),
        "cutoff_date": split.cutoff_date,
        "results": results,
    }

    report_path = Path(
        "data/reports/"
        "intermittent_baseline_evaluation.json"
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
        f"Report:                 "
        f"{report_path.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()