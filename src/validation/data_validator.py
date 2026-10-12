from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationIssue:
    severity: str
    table: str
    field: str
    message: str
    row_number: int | None = None


@dataclass
class ValidationReport:
    table: str
    row_count: int
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == "error"
        ]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == "warning"
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "table": self.table,
            "row_count": self.row_count,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "issues": [
                {
                    "severity": issue.severity,
                    "table": issue.table,
                    "field": issue.field,
                    "message": issue.message,
                    "row_number": issue.row_number,
                }
                for issue in self.issues
            ],
        }


class DataValidator:
    """
    V1 validation only.

    Important:
    Validation reports problems.
    It does not silently repair source data.
    """

    REQUIRED_ID_TABLES = {
        "orders",
        "menus",
        "stock_managements",
        "stock_logs",
        "stock_requirements",
    }

    def validate(
        self,
        table: str,
        rows: list[dict[str, Any]],
    ) -> ValidationReport:

        report = ValidationReport(
            table=table,
            row_count=len(rows),
        )

        self._validate_ids(table, rows, report)
        self._validate_nulls(table, rows, report)

        if table == "orders":
            self._validate_orders(rows, report)

        if table == "stock_managements":
            self._validate_inventory(rows, report)

        if table == "stock_requirements":
            self._validate_stock_requirements(rows, report)

        return report

    def _validate_ids(
        self,
        table: str,
        rows: list[dict[str, Any]],
        report: ValidationReport,
    ) -> None:

        if table not in self.REQUIRED_ID_TABLES:
            return

        seen: set[Any] = set()

        for index, row in enumerate(rows, start=1):
            value = row.get("id")

            if value is None:
                report.issues.append(
                    ValidationIssue(
                        severity="error",
                        table=table,
                        field="id",
                        message="Primary key is NULL",
                        row_number=index,
                    )
                )
                continue

            if value in seen:
                report.issues.append(
                    ValidationIssue(
                        severity="error",
                        table=table,
                        field="id",
                        message=f"Duplicate primary key: {value}",
                        row_number=index,
                    )
                )

            seen.add(value)

    def _validate_nulls(
        self,
        table: str,
        rows: list[dict[str, Any]],
        report: ValidationReport,
    ) -> None:

        if not rows:
            report.issues.append(
                ValidationIssue(
                    severity="error",
                    table=table,
                    field="*",
                    message="Table contains zero rows",
                )
            )

    def _validate_orders(
        self,
        rows: list[dict[str, Any]],
        report: ValidationReport,
    ) -> None:

        valid_order_types = {
            "dine_in",
            "takeaway",
            "delivery",
        }

        for index, row in enumerate(rows, start=1):

            order_type = row.get("order_type")

            if order_type not in valid_order_types:
                report.issues.append(
                    ValidationIssue(
                        severity="error",
                        table="orders",
                        field="order_type",
                        message=f"Unknown order type: {order_type!r}",
                        row_number=index,
                    )
                )

            order_items = row.get("order_items")

            if not isinstance(order_items, str):
                report.issues.append(
                    ValidationIssue(
                        severity="error",
                        table="orders",
                        field="order_items",
                        message="order_items is not a string",
                        row_number=index,
                    )
                )
                continue

            try:
                parsed = json.loads(order_items)

                if not isinstance(parsed, list):
                    report.issues.append(
                        ValidationIssue(
                            severity="error",
                            table="orders",
                            field="order_items",
                            message="order_items JSON is not an array",
                            row_number=index,
                        )
                    )

            except json.JSONDecodeError as exc:
                report.issues.append(
                    ValidationIssue(
                        severity="error",
                        table="orders",
                        field="order_items",
                        message=f"Invalid JSON: {exc}",
                        row_number=index,
                    )
                )

    def _validate_inventory(
        self,
        rows: list[dict[str, Any]],
        report: ValidationReport,
    ) -> None:

        for index, row in enumerate(rows, start=1):

            quantity = row.get("quantity")

            if quantity is not None and quantity < 0:
                report.issues.append(
                    ValidationIssue(
                        severity="warning",
                        table="stock_managements",
                        field="quantity",
                        message=(
                            "Negative inventory quantity detected. "
                            "Value preserved exactly; business semantics "
                            "must be resolved later."
                        ),
                        row_number=index,
                    )
                )

    def _validate_stock_requirements(
        self,
        rows: list[dict[str, Any]],
        report: ValidationReport,
    ) -> None:

        for index, row in enumerate(rows, start=1):

            if row.get("quantity") is None:
                report.issues.append(
                    ValidationIssue(
                        severity="warning",
                        table="stock_requirements",
                        field="quantity",
                        message="Requirement quantity is NULL",
                        row_number=index,
                    )
                )