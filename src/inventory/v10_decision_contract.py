from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryDecisionInput:
    item_id: int
    restaurant: int
    forecast_demand: float
    current_stock: float
    standard_deviation: float
    confirmed_incoming: float = 0.0
    pack_size: float = 1.0
    minimum_order_quantity: float = 0.0

    def __post_init__(self) -> None:
        if self.item_id <= 0:
            raise ValueError("item_id must be positive")

        if self.restaurant <= 0:
            raise ValueError("restaurant must be positive")

        values = {
            "forecast_demand": self.forecast_demand,
            "current_stock": self.current_stock,
            "standard_deviation": self.standard_deviation,
            "confirmed_incoming": self.confirmed_incoming,
            "pack_size": self.pack_size,
            "minimum_order_quantity": self.minimum_order_quantity,
        }

        for name, value in values.items():
            if value < 0:
                raise ValueError(f"{name} cannot be negative")

        if self.pack_size <= 0:
            raise ValueError("pack_size must be positive")
