from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseOrderLine:
    item_id: int
    restaurant: int
    quantity: float
    pack_size: float

    def __post_init__(self) -> None:
        if self.item_id <= 0:
            raise ValueError("item_id must be positive")

        if self.restaurant <= 0:
            raise ValueError("restaurant must be positive")

        if self.quantity < 0:
            raise ValueError("quantity cannot be negative")

        if self.pack_size <= 0:
            raise ValueError("pack_size must be positive")

        if self.quantity > 0:
            remainder = self.quantity % self.pack_size
            if abs(remainder) > 1e-9:
                raise ValueError(
                    "purchase quantity must be aligned to pack_size"
                )
