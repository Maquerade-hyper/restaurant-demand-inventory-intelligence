from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyStockResult:
    safety_stock: float
    method: str


class SafetyStockCalculator:
    def calculate(
        self,
        standard_deviation: float,
        multiplier: float = 1.96,
    ) -> SafetyStockResult:
        if standard_deviation < 0:
            raise ValueError(
                "standard_deviation cannot be negative"
            )

        if multiplier < 0:
            raise ValueError(
                "multiplier cannot be negative"
            )

        return SafetyStockResult(
            safety_stock=(
                standard_deviation * multiplier
            ),
            method="forecast_standard_deviation",
        )
