from __future__ import annotations

import math
from collections.abc import Callable

from src.forecasting.recursive_future_feature_builder import (
    RecursiveFutureFeatureRow,
)


class PredictionAdapter:
    def __init__(
        self,
        predictor: Callable[[RecursiveFutureFeatureRow], float],
    ) -> None:
        if not callable(predictor):
            raise TypeError("predictor must be callable")

        self.predictor = predictor

    def predict(
        self,
        features: RecursiveFutureFeatureRow,
    ) -> float:
        prediction = float(self.predictor(features))

        if not math.isfinite(prediction):
            raise ValueError("prediction must be finite")

        if prediction < 0:
            raise ValueError("prediction must be non-negative")

        return prediction
