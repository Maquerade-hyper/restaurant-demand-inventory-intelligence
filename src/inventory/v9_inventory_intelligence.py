from __future__ import annotations

from dataclasses import dataclass

from src.inventory.v9_purchase_recommendation import (
    PurchaseRecommendation,
    PurchaseRecommendationService,
)
from src.inventory.v9_safety_stock import (
    SafetyStockCalculator,
    SafetyStockResult,
)
from src.inventory.v9_stockout_risk import (
    StockoutRisk,
    StockoutRiskAnalyzer,
)
from src.inventory.v9_excess_stock_risk import (
    ExcessStockRisk,
    ExcessStockRiskAnalyzer,
)


@dataclass(frozen=True)
class InventoryIntelligence:
    safety_stock: SafetyStockResult
    purchase: PurchaseRecommendation
    stockout: StockoutRisk
    excess_stock: ExcessStockRisk


class InventoryIntelligenceService:
    def __init__(self) -> None:
        self.safety_stock = SafetyStockCalculator()
        self.purchase = PurchaseRecommendationService()
        self.stockout = StockoutRiskAnalyzer()
        self.excess = ExcessStockRiskAnalyzer()

    def analyze(
        self,
        forecast_demand: float,
        current_stock: float,
        standard_deviation: float,
        confirmed_incoming: float = 0.0,
        pack_size: float = 1.0,
        minimum_order_quantity: float = 0.0,
    ) -> InventoryIntelligence:
        safety = self.safety_stock.calculate(
            standard_deviation=standard_deviation
        )

        purchase = self.purchase.recommend(
            forecast_demand=forecast_demand,
            current_stock=current_stock,
            safety_stock=safety.safety_stock,
            confirmed_incoming=confirmed_incoming,
            pack_size=pack_size,
            minimum_order_quantity=minimum_order_quantity,
        )

        stockout = self.stockout.analyze(
            current_stock=current_stock,
            confirmed_incoming=confirmed_incoming,
            forecast_demand=forecast_demand,
        )

        excess = self.excess.analyze(
            current_stock=current_stock,
            forecast_demand=forecast_demand,
            safety_stock=safety.safety_stock,
        )

        return InventoryIntelligence(
            safety_stock=safety,
            purchase=purchase,
            stockout=stockout,
            excess_stock=excess,
        )
