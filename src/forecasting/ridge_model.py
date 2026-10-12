from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.linear_model import Ridge

from src.forecasting.model_interface import ForecastModel


class RidgeDemandModel(ForecastModel):
    name = "ridge"

    FEATURE_COLUMNS = [
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_mean_28",
        "rolling_max_7",
        "rolling_std_7",
        "day_of_week",
        "day_of_month",
        "month",
        "is_weekend",
    ]

    def __init__(self, alpha: float = 1.0):
        if alpha <= 0:
            raise ValueError(
                "alpha must be greater than 0"
            )

        self.alpha = alpha
        self.model = Ridge(alpha=alpha)
        self.fitted = False

    def _features(
        self,
        rows: list[dict[str, Any]],
    ) -> np.ndarray:
        return np.asarray(
            [
                [
                    float(row[column])
                    for column in self.FEATURE_COLUMNS
                ]
                for row in rows
            ],
            dtype=float,
        )

    def fit(
        self,
        rows: list[dict[str, Any]],
    ) -> None:
        if not rows:
            raise ValueError(
                "Training rows cannot be empty"
            )

        X = self._features(rows)

        y = np.asarray(
            [
                float(row["demand_quantity"])
                for row in rows
            ],
            dtype=float,
        )

        self.model.fit(X, y)
        self.fitted = True

    def predict(
        self,
        rows: list[dict[str, Any]],
    ) -> list[float]:
        if not self.fitted:
            raise RuntimeError(
                "Model has not been fitted"
            )

        if not rows:
            return []

        X = self._features(rows)

        predictions = self.model.predict(X)

        # Demand cannot be negative.
        predictions = np.maximum(
            predictions,
            0.0,
        )

        return predictions.tolist() 