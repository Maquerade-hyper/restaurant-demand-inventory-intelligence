from __future__ import annotations

from src.forecasting.forecast_run_result import ForecastRunResult


class ForecastResultValidator:
    def validate(
        self,
        result: ForecastRunResult,
    ) -> None:
        if result.restaurant <= 0:
            raise ValueError("restaurant must be positive")

        if result.item_id <= 0:
            raise ValueError("item_id must be positive")

        if result.horizon <= 0:
            raise ValueError("horizon must be positive")

        if len(result.predictions) != result.horizon:
            raise ValueError(
                "prediction count must equal horizon"
            )

        dates = [
            prediction.date
            for prediction in result.predictions
        ]

        if len(set(dates)) != len(dates):
            raise ValueError(
                "prediction dates must be unique"
            )

        for prediction in result.predictions:
            if prediction.restaurant != result.restaurant:
                raise ValueError(
                    "prediction restaurant mismatch"
                )

            if prediction.item_id != result.item_id:
                raise ValueError(
                    "prediction item mismatch"
                )

            if prediction.prediction < 0:
                raise ValueError(
                    "prediction must be non-negative"
                )
