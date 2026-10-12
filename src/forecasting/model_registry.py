from __future__ import annotations

from typing import Type

from src.forecasting.model_interface import ForecastModel


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, Type[ForecastModel]] = {}

    def register(
        self,
        model_class: Type[ForecastModel],
    ) -> None:
        name = model_class.name

        if not name:
            raise ValueError(
                "Model class must define a name"
            )

        if name in self._models:
            raise ValueError(
                f"Model already registered: {name}"
            )

        self._models[name] = model_class

    def get(
        self,
        name: str,
    ) -> Type[ForecastModel]:
        if name not in self._models:
            raise KeyError(
                f"Unknown model: {name}"
            )

        return self._models[name]

    def names(self) -> list[str]:
        return sorted(self._models.keys())

    def contains(self, name: str) -> bool:
        return name in self._models