from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StockoutRisk:
    risk: bool
    available_quantity: float
    forecast_demand: float


class StockoutRiskAnalyzer:
    def analyze(
        self,
        current_stock: float,
        confirmed_incoming: float,
        forecast_demand: float,
    ) -> StockoutRisk:
        if current_stock < 0:
            raise ValueError(
                "current_stock cannot be negative"
            )

        if confirmed_incoming < 0:
            raise ValueError(
                "confirmed_incoming cannot be negative"
            )

        if forecast_demand < 0:
            raise ValueError(
                "forecast_demand cannot be negative"
            )

        available = (
            current_stock
            + confirmed_incoming
        )

        return StockoutRisk(
            risk=available < forecast_demand,
            available_quantity=available,
            forecast_demand=forecast_demand,
        )
