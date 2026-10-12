from __future__ import annotations

from dataclasses import dataclass

from src.inventory.v9_inventory_contract import (
    InventoryDemandInput,
)


@dataclass(frozen=True)
class NetRequirementResult:
    net_requirement: float


class NetRequirementCalculator:
    def calculate(
        self,
        demand: InventoryDemandInput,
    ) -> NetRequirementResult:
        requirement = (
            demand.forecast_demand
            + demand.safety_stock
            - demand.current_stock
            - demand.confirmed_incoming
        )

        return NetRequirementResult(
            net_requirement=max(0.0, requirement)
        )
