from dataclasses import dataclass, asdict
from typing import Any

from .v10_action_plan import InventoryActionPlan
from .v10_decision_contract import InventoryDecisionInput
from .v10_decision_validator import DecisionValidationResult
from .v10_purchase_order import PurchaseOrderLine
from .v9_inventory_intelligence import InventoryIntelligence


@dataclass(frozen=True)
class InventoryIntelligencePackage:
    version: str
    decision_input: InventoryDecisionInput
    intelligence: InventoryIntelligence
    purchase_line: PurchaseOrderLine | None
    action_plan: InventoryActionPlan
    validation: DecisionValidationResult

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
