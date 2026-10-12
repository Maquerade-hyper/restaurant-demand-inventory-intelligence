from collections import defaultdict
from typing import Any

from src.forecasting.baselines import build_baseline_forecasts
from src.forecasting.metrics import evaluate


class BaselineEvaluator:
    def __init__(
        self,
        train: list[dict[str, Any]],
        test: list[dict[str, Any]],
    ) -> None:
        self.train = train
        self.test = test

    def evaluate(self) -> dict[str, dict[str, float]]:
        train_groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]],
        ] = defaultdict(list)

        test_groups: dict[
            tuple[Any, Any],
            list[dict[str, Any]],
        ] = defaultdict(list)

        # Group training rows by restaurant + item.
        for row in self.train:
            key = (
                row.get("restaurant"),
                row.get("item_id"),
            )

            train_groups[key].append(row)

        # Group test rows by restaurant + item.
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

        # Generate forecasts independently for every
        # restaurant/item time series.
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

            horizon = len(test_rows)

            forecasts = build_baseline_forecasts(
                history,
                horizon,
            )

            actual = [
                float(row["demand_quantity"])
                for row in test_rows
            ]

            for model_name, forecast in forecasts.items():
                actuals[model_name].extend(actual)

                predictions[model_name].extend(
                    forecast
                )

        # Preserve the Part 13 evaluator contract:
        #
        # {
        #     "naive": {
        #         "mae": ...,
        #         "rmse": ...,
        #         "smape": ...
        #     }
        # }
        #
        # Segment analysis is handled separately by
        # evaluate_segments().
        results: dict[
            str,
            dict[str, float],
        ] = {}

        for model_name in actuals:
            results[model_name] = evaluate(
                actuals[model_name],
                predictions[model_name],
            )

        return results

    def evaluate_segments(
        self,
    ) -> dict[
        str,
        dict[str, dict[str, float]],
    ]:
        """
        Evaluate each baseline across:
        - all observations
        - zero-actual observations
        - positive-actual observations
        """

        from src.forecasting.metrics import evaluate_segments

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

            horizon = len(test_rows)

            forecasts = build_baseline_forecasts(
                history,
                horizon,
            )

            actual = [
                float(row["demand_quantity"])
                for row in test_rows
            ]

            for model_name, forecast in forecasts.items():
                actuals[model_name].extend(actual)

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