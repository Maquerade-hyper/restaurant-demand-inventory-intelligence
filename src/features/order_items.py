from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class OrderItemRecord:
    order_id: int | None
    order_date: str | None
    restaurant: Any
    order_type: Any
    payment_status: Any
    order_status: Any

    item_id: int | None
    item_name: str | None
    quantity: float
    item_price: float | None


class OrderItemDatasetBuilder:
    """
    Converts canonical orders into one row per ordered item.

    Important:
    - Does not aggregate demand.
    - Does not merge items by name.
    - Does not infer missing menu relationships.
    - Preserves item_id and item_name separately.
    """

    def __init__(self, orders: list[dict[str, Any]]):
        self.orders = orders

    @staticmethod
    def _number(value: Any) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _integer(value: Any) -> int | None:
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _date(value: Any) -> str | None:
        if value is None:
            return None

        text = str(value).strip()

        if not text:
            return None

        # Canonical timestamps use ISO-like format.
        try:
            parsed = datetime.fromisoformat(text)
            return parsed.date().isoformat()
        except ValueError:
            # Preserve the original value rather than inventing a date.
            return text[:10] if len(text) >= 10 else text

    def build(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []

        for order in self.orders:
            order_id = self._integer(order.get("id"))
            order_date = self._date(order.get("created_at"))
            restaurant = order.get("restaurant")
            order_type = order.get("order_type")
            payment_status = order.get("payment_status")
            order_status = order.get("status")

            items = order.get("order_items")

            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue

                item_id = self._integer(item.get("id"))
                item_name = item.get("item_name")

                quantity = self._number(item.get("quantity"))

                if quantity is None:
                    continue

                item_price = self._number(item.get("item_price"))

                record = OrderItemRecord(
                    order_id=order_id,
                    order_date=order_date,
                    restaurant=restaurant,
                    order_type=order_type,
                    payment_status=payment_status,
                    order_status=order_status,
                    item_id=item_id,
                    item_name=item_name,
                    quantity=quantity,
                    item_price=item_price,
                )

                records.append(record.__dict__)

        return records