from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IncomingStock:
    quantity: float
    expected_date: str | None = None
    confirmed: bool = False

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError(
                "incoming quantity cannot be negative"
            )


class IncomingStockCalculator:
    def confirmed_quantity(
        self,
        incoming: list[IncomingStock],
    ) -> float:
        return sum(
            item.quantity
            for item in incoming
            if item.confirmed
        )

    def total_quantity(
        self,
        incoming: list[IncomingStock],
    ) -> float:
        return sum(
            item.quantity
            for item in incoming
        )
