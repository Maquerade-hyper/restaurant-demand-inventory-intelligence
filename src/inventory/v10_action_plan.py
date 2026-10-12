from dataclasses import dataclass

from .v10_purchase_order import PurchaseOrderLine


@dataclass(frozen=True)
class InventoryActionPlan:
    action: str
    purchase_required: bool
    purchase_line: PurchaseOrderLine | None
    stockout_risk: bool
    excess_stock_risk: bool

    def __post_init__(self) -> None:
        allowed = {
            "purchase",
            "hold",
            "review_stockout",
            "review_excess",
        }

        if self.action not in allowed:
            raise ValueError(f"unsupported action: {self.action}")

        if self.purchase_required and self.purchase_line is None:
            raise ValueError(
                "purchase_line is required when purchase is required"
            )

        if not self.purchase_required and self.purchase_line is not None:
            raise ValueError(
                "purchase_line must be None when purchase is not required"
            )
