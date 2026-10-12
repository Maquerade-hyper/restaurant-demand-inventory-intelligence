from .v10_action_plan import InventoryActionPlan
from .v10_decision_contract import InventoryDecisionInput
from .v10_decision_validator import InventoryDecisionValidator
from .v10_intelligence_package import InventoryIntelligencePackage
from .v10_purchase_order import PurchaseOrderLine
from .v9_inventory_intelligence import InventoryIntelligenceService


class InventoryDecisionService:

    def __init__(self) -> None:
        self.inventory_service = InventoryIntelligenceService()
        self.validator = InventoryDecisionValidator()

    def build(
        self,
        decision_input: InventoryDecisionInput,
    ) -> InventoryIntelligencePackage:

        intelligence = self.inventory_service.analyze(
            forecast_demand=decision_input.forecast_demand,
            current_stock=decision_input.current_stock,
            standard_deviation=decision_input.standard_deviation,
            confirmed_incoming=decision_input.confirmed_incoming,
            pack_size=decision_input.pack_size,
            minimum_order_quantity=decision_input.minimum_order_quantity,
        )

        purchase_line = None

        if intelligence.purchase.should_purchase:
            purchase_line = PurchaseOrderLine(
                item_id=decision_input.item_id,
                restaurant=decision_input.restaurant,
                quantity=intelligence.purchase.recommended_quantity,
                pack_size=decision_input.pack_size,
            )

        if intelligence.stockout.risk:
            if intelligence.purchase.should_purchase:
                action = "purchase"
            else:
                action = "review_stockout"
        elif intelligence.excess_stock.risk:
            action = "review_excess"
        else:
            action = "hold"

        action_plan = InventoryActionPlan(
            action=action,
            purchase_required=intelligence.purchase.should_purchase,
            purchase_line=purchase_line,
            stockout_risk=intelligence.stockout.risk,
            excess_stock_risk=intelligence.excess_stock.risk,
        )

        validation = self.validator.validate(
            decision_input,
            action_plan,
        )

        return InventoryIntelligencePackage(
            version="V10",
            decision_input=decision_input,
            intelligence=intelligence,
            purchase_line=purchase_line,
            action_plan=action_plan,
            validation=validation,
        )
