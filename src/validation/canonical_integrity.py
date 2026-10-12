from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class IntegrityIssue:
    table: str
    field: str
    value: Any
    issue: str
    severity: str = "WARNING"


class CanonicalIntegrityValidator:
    """
    Validates relationships that are actually supported by the source data.

    Important:
    - Never invent foreign-key relationships.
    - Never modify source data.
    - Missing menu references are reported.
    - stock_logs.item is NOT assumed to be menus.id.
    """

    def __init__(self, data: dict[str, list[dict[str, Any]]]):
        self.data = data
        self.issues: list[IntegrityIssue] = []

    def _menu_ids(self) -> set[Any]:
        return {
            row.get("id")
            for row in self.data.get("menus", [])
            if row.get("id") is not None
        }

    def validate_menu_ids(self) -> None:
        seen: set[Any] = set()

        for row in self.data.get("menus", []):
            menu_id = row.get("id")

            if menu_id is None:
                self.issues.append(
                    IntegrityIssue(
                        table="menus",
                        field="id",
                        value=None,
                        issue="missing menu ID",
                        severity="ERROR",
                    )
                )
                continue

            if menu_id in seen:
                self.issues.append(
                    IntegrityIssue(
                        table="menus",
                        field="id",
                        value=menu_id,
                        issue="duplicate menu ID",
                        severity="ERROR",
                    )
                )

            seen.add(menu_id)

    def validate_order_item_references(self) -> None:
        """
        order_items.id is supported as a menu/item reference by
        the order data structure.

        Missing IDs are reported, never repaired.
        """

        menu_ids = self._menu_ids()

        for order in self.data.get("orders", []):
            order_id = order.get("id")
            items = order.get("order_items")

            if items is None:
                continue

            if not isinstance(items, list):
                self.issues.append(
                    IntegrityIssue(
                        table="orders",
                        field="order_items",
                        value=order_id,
                        issue="order_items is not a list",
                        severity="ERROR",
                    )
                )
                continue

            for item in items:
                if not isinstance(item, dict):
                    self.issues.append(
                        IntegrityIssue(
                            table="orders",
                            field="order_items",
                            value=order_id,
                            issue="order item is not an object",
                            severity="ERROR",
                        )
                    )
                    continue

                item_id = item.get("id")

                if item_id is None:
                    self.issues.append(
                        IntegrityIssue(
                            table="orders",
                            field="order_items.id",
                            value=order_id,
                            issue="missing item ID",
                            severity="WARNING",
                        )
                    )
                    continue

                if item_id not in menu_ids:
                    self.issues.append(
                        IntegrityIssue(
                            table="orders",
                            field="order_items.id",
                            value=item_id,
                            issue=(
                                "item ID is not present in the "
                                "current menu snapshot"
                            ),
                            severity="WARNING",
                        )
                    )

    def validate_stock_requirement_references(self) -> None:
        """
        stock_requirements.item_id is treated as an item reference.

        We report missing menu IDs but do not assume that the
        item belongs to the menu table permanently.
        """

        menu_ids = self._menu_ids()

        for row in self.data.get("stock_requirements", []):
            item_id = row.get("item_id")

            if item_id is None:
                continue

            if item_id not in menu_ids:
                self.issues.append(
                    IntegrityIssue(
                        table="stock_requirements",
                        field="item_id",
                        value=item_id,
                        issue=(
                            "item ID is not present in the "
                            "current menu snapshot"
                        ),
                        severity="WARNING",
                    )
                )

    def validate_stock_logs(self) -> None:
        """
        Do NOT validate stock_logs.item against menus.id.

        The source data does not establish that relationship.
        """

        return

    def validate(self) -> list[IntegrityIssue]:
        self.issues = []

        self.validate_menu_ids()
        self.validate_order_item_references()
        self.validate_stock_requirement_references()
        self.validate_stock_logs()

        return self.issues

    def errors(self) -> list[IntegrityIssue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == "ERROR"
        ]

    def warnings(self) -> list[IntegrityIssue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == "WARNING"
        ]