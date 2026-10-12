from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InventoryState:
    item_id: int
    restaurant: int
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        if self.item_id <= 0:
            raise ValueError("item_id must be positive")

        if self.restaurant <= 0:
            raise ValueError("restaurant must be positive")

        if self.quantity < 0:
            raise ValueError("quantity cannot be negative")

        if not self.unit.strip():
            raise ValueError("unit cannot be empty")
