from __future__ import annotations

from dataclasses import dataclass

from src.inventory.v9_net_requirement import (
    NetRequirementCalculator,
)
from src.inventory.v9_purchase_quantity import (
    PurchaseQuantityCalculator,
)


@dataclass(frozen=True)
class PurchaseRecommendation:
    net_requirement: float
    recommended_quantity: float
    should_purchase: bool


class PurchaseRecommendationService:
    def __init__(self) -> None:
        self.net_requirement = NetRequirementCalculator()
        self.purchase_quantity = PurchaseQuantityCalculator()

    def recommend(
        self,
        forecast_demand: float,
        current_stock: float,
        safety_stock: float,
        confirmed_incoming: float,
        pack_size: float = 1.0,
        minimum_order_quantity: float = 0.0,
    ) -> PurchaseRecommendation:
        from src.inventory.v9_inventory_contract import (
            InventoryDemandInput,
        )

        demand = InventoryDemandInput(
            forecast_demand=forecast_demand,
            current_stock=current_stock,
            confirmed_incoming=confirmed_incoming,
            safety_stock=safety_stock,
        )

        requirement = self.net_requirement.calculate(
            demand
        )

        purchase = self.purchase_quantity.calculate(
            net_requirement=requirement.net_requirement,
            pack_size=pack_size,
            minimum_order_quantity=minimum_order_quantity,
        )

        return PurchaseRecommendation(
            net_requirement=requirement.net_requirement,
            recommended_quantity=purchase.rounded_quantity,
            should_purchase=(
                purchase.rounded_quantity > 0
            ),
        )
