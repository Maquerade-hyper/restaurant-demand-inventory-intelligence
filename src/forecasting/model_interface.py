from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ForecastModel(ABC):
    """
    Common interface for all forecasting models.

    Every model must:
    1. train on historical rows
    2. generate predictions from feature rows
    """

    name: str = "base"

    @abstractmethod
    def fit(self, rows: list[dict[str, Any]]) -> None:
        """Train the model."""
        raise NotImplementedError

    @abstractmethod
    def predict(
        self,
        rows: list[dict[str, Any]],
    ) -> list[float]:
        """Generate predictions."""
        raise NotImplementedError

    def fit_predict(
        self,
        train_rows: list[dict[str, Any]],
        prediction_rows: list[dict[str, Any]],
    ) -> list[float]:
        self.fit(train_rows)
        return self.predict(prediction_rows)