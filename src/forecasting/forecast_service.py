from __future__ import annotations

from typing import Any

from src.forecasting.model_predictor import ModelPredictor
from src.forecasting.model_registry import ModelRegistry
from src.forecasting.model_trainer import ModelTrainer


class ForecastService:
    def __init__(
        self,
        registry: ModelRegistry,
    ):
        self.registry = registry
        self.trainer = ModelTrainer(registry)
        self.predictor = ModelPredictor()

    def train_and_predict(
        self,
        model_name: str,
        train_rows: list[dict[str, Any]],
        prediction_rows: list[dict[str, Any]],
        **model_kwargs: Any,
    ) -> list[float]:
        model = self.trainer.train(
            model_name,
            train_rows,
            **model_kwargs,
        )

        return self.predictor.predict(
            model,
            prediction_rows,
        )