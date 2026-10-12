from __future__ import annotations

from typing import Any

from src.forecasting.model_interface import ForecastModel


class ModelPredictor:
    def predict(
        self,
        model: ForecastModel,
        rows: list[dict[str, Any]],
    ) -> list[float]:
        if not model.fitted:
            raise RuntimeError(
                f"Model '{model.name}' has not been fitted"
            )

        if not rows:
            return []

        predictions = model.predict(rows)

        if len(predictions) != len(rows):
            raise ValueError(
                "Prediction count does not match input row count"
            )

        validated: list[float] = []

        for index, prediction in enumerate(predictions):
            value = float(prediction)

            if value < 0:
                raise ValueError(
                    f"Negative prediction at row {index}: {value}"
                )

            validated.append(value)

        return validated