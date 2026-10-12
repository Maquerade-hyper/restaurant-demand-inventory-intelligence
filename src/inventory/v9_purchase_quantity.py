from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PurchaseQuantityResult:
    quantity: float
    rounded_quantity: float


class PurchaseQuantityCalculator:
    def calculate(
        self,
        net_requirement: float,
        pack_size: float = 1.0,
        minimum_order_quantity: float = 0.0,
    ) -> PurchaseQuantityResult:
        if net_requirement < 0:
            raise ValueError(
                "net_requirement cannot be negative"
            )

        if pack_size <= 0:
            raise ValueError(
                "pack_size must be positive"
            )

        if minimum_order_quantity < 0:
            raise ValueError(
                "minimum_order_quantity cannot be negative"
            )

        if net_requirement == 0:
            return PurchaseQuantityResult(
                quantity=0.0,
                rounded_quantity=0.0,
            )

        required = max(
            net_requirement,
            minimum_order_quantity,
        )

        rounded = (
            math.ceil(required / pack_size)
            * pack_size
        )

        return PurchaseQuantityResult(
            quantity=net_requirement,
            rounded_quantity=float(rounded),
        )
