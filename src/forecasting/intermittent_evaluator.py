from collections import defaultdict
from typing import Any

from src.forecasting.intermittent_baselines import (
    build_intermittent_forecasts,
)
from src.forecasting.metrics import evaluate_segments


class IntermittentBaselineEvaluator:
    def __init__(
        self,
        train: list[dict[str, Any]],
        test: list[dict[str, Any]],
    ) -> None:
        self.train = train
        self.test = test

    def evaluate(
        self,
    ) -> dict[
        str,
        dict[str, dict[str, float]],
    ]:
        train_groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]],
        ] = defaultdict(list)

        test_groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]],
        ] = defaultdict(list)

        for row in self.train:
            key = (
                row.get("restaurant"),
                row.get("item_id"),
            )

            train_groups[key].append(row)

        for row in self.test:
            key = (
                row.get("restaurant"),
                row.get("item_id"),
            )

            test_groups[key].append(row)

        actuals: dict[
            str,
            list[float],
        ] = defaultdict(list)

        predictions: dict[
            str,
            list[float],
        ] = defaultdict(list)

        for key, test_rows in test_groups.items():
            test_rows.sort(
                key=lambda row: row["date"]
            )

            history_rows = train_groups.get(
                key,
                [],
            )

            history_rows.sort(
                key=lambda row: row["date"]
            )

            history = [
                float(row["demand_quantity"])
                for row in history_rows
            ]

            actual = [
                float(row["demand_quantity"])
                for row in test_rows
            ]

            forecasts = build_intermittent_forecasts(
                history,
                len(test_rows),
            )

            for model_name, forecast in forecasts.items():
                actuals[model_name].extend(
                    actual
                )

                predictions[model_name].extend(
                    forecast
                )

        results: dict[
            str,
            dict[str, dict[str, float]],
        ] = {}

        for model_name in actuals:
            results[model_name] = evaluate_segments(
                actuals[model_name],
                predictions[model_name],
            )

        return results