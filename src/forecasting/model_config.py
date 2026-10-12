
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    model_name: str
    alpha: float
    feature_columns: list[str]
    target_column: str
    validation_days: int


RIDGE_FEATURES = [
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


def build_ridge_config(
    alpha: float = 100.0,
) -> ModelConfig:
    if alpha <= 0:
        raise ValueError(
            "alpha must be greater than 0"
        )

    return ModelConfig(
        model_name="ridge",
        alpha=alpha,
        feature_columns=list(RIDGE_FEATURES),
        target_column="demand_quantity",
        validation_days=14,
    )