from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExcessStockRisk:
    risk: bool
    excess_quantity: float


class ExcessStockRiskAnalyzer:
    def analyze(
        self,
        current_stock: float,
        forecast_demand: float,
        safety_stock: float,
    ) -> ExcessStockRisk:
        if current_stock < 0:
            raise ValueError(
                "current_stock cannot be negative"
            )

        if forecast_demand < 0:
            raise ValueError(
                "forecast_demand cannot be negative"
            )

        if safety_stock < 0:
            raise ValueError(
                "safety_stock cannot be negative"
            )

        target_stock = (
            forecast_demand
            + safety_stock
        )

        excess = max(
            0.0,
            current_stock - target_stock,
        )

        return ExcessStockRisk(
            risk=excess > 0,
            excess_quantity=excess,
        )
