from __future__ import annotations

from typing import Any

from src.forecasting.model_registry import ModelRegistry


class ModelTrainer:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry

    def train(
        self,
        model_name: str,
        train_rows: list[dict[str, Any]],
        **model_kwargs: Any,
    ):
        if not train_rows:
            raise ValueError(
                "Training rows cannot be empty"
            )

        model_class = self.registry.get(
            model_name
        )

        model = model_class(
            **model_kwargs
        )

        model.fit(train_rows)

        return model