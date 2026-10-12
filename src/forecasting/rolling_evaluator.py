from typing import Any

from src.forecasting.baseline_evaluator import (
    BaselineEvaluator,
)
from src.forecasting.intermittent_evaluator import (
    IntermittentBaselineEvaluator,
)
from src.forecasting.rolling_backtest import (
    RollingBacktester,
)


class RollingEvaluator:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        test_days: int = 14,
        windows: int = 3,
    ) -> None:
        self.rows = rows
        self.test_days = test_days
        self.windows = windows

    def evaluate(
        self,
    ) -> list[dict[str, Any]]:
        backtester = RollingBacktester(
            self.rows,
            test_days=self.test_days,
            windows=self.windows,
        )

        rolling_windows = backtester.split()

        results: list[dict[str, Any]] = []

        for index, window in enumerate(
            rolling_windows,
            start=1,
        ):
            baseline_evaluator = (
                BaselineEvaluator(
                    window.train,
                    window.test,
                )
            )

            intermittent_evaluator = (
                IntermittentBaselineEvaluator(
                    window.train,
                    window.test,
                )
            )

            baseline_results = (
                baseline_evaluator
                .evaluate_segments()
            )

            intermittent_results = (
                intermittent_evaluator
                .evaluate()
            )

            results.append(
                {
                    "window": index,
                    "cutoff_date": (
                        window.cutoff_date
                    ),
                    "train_rows": len(
                        window.train
                    ),
                    "test_rows": len(
                        window.test
                    ),
                    "baseline_results": (
                        baseline_results
                    ),
                    "intermittent_results": (
                        intermittent_results
                    ),
                }
            )

        return results