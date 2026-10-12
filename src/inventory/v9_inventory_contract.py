from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryDemandInput:
    forecast_demand: float
    current_stock: float
    confirmed_incoming: float = 0.0
    safety_stock: float = 0.0

    def __post_init__(self) -> None:
        if self.forecast_demand < 0:
            raise ValueError("forecast_demand cannot be negative")

        if self.current_stock < 0:
            raise ValueError("current_stock cannot be negative")

        if self.confirmed_incoming < 0:
            raise ValueError(
                "confirmed_incoming cannot be negative"
            )

        if self.safety_stock < 0:
            raise ValueError(
                "safety_stock cannot be negative"
            )
