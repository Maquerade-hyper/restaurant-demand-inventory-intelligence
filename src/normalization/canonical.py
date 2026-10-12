from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CanonicalNormalizer:
    """
    Converts V1 extracted JSON records into a stable canonical representation.

    Important:
    - Does not merge records.
    - Does not infer item identity from names.
    - Does not change business meaning.
    - Preserves source record IDs.
    - Preserves unknown/source fields.
    """

    def __init__(self, extracted_dir: Path):
        self.extracted_dir = Path(extracted_dir)

    def load(self, table: str) -> list[dict[str, Any]]:
        path = self.extracted_dir / f"{table}.json"

        if not path.exists():
            raise FileNotFoundError(f"Extracted file not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and "rows" in data:
            records = data["rows"]
        elif isinstance(data, dict) and "records" in data:
            records = data["records"]
        elif isinstance(data, list):
            records = data
        else:
            raise ValueError(
                f"Unsupported extracted format for {table}: "
                f"{type(data).__name__}"
            )

        if not isinstance(records, list):
            raise ValueError(f"{table}.records must be a list")

        return records

    @staticmethod
    def normalize_id(value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            value = value.strip()

            if value.isdigit():
                return int(value)

        return value

    @staticmethod
    def normalize_timestamp(value: Any) -> Any:
        if value is None:
            return None

        if not isinstance(value, str):
            return value

        value = value.strip()

        if not value:
            return None

        # Keep the original semantic timestamp while making
        # the separator consistent.
        return value.replace(" ", "T", 1)

    @staticmethod
    def normalize_order_items(value: Any) -> list[dict[str, Any]] | None:
        if value is None:
            return None

        if isinstance(value, list):
            items = value
        elif isinstance(value, str):
            value = value.strip()

            if not value:
                return None

            try:
                items = json.loads(value)
            except json.JSONDecodeError:
                return None
        else:
            return None

        if not isinstance(items, list):
            return None

        normalized: list[dict[str, Any]] = []

        for item in items:
            if not isinstance(item, dict):
                normalized.append(item)
                continue

            record = dict(item)

            if "id" in record:
                record["id"] = CanonicalNormalizer.normalize_id(
                    record["id"]
                )

            if "quantity" in record:
                record["quantity"] = CanonicalNormalizer.normalize_number(
                    record["quantity"]
                )

            if "item_price" in record:
                record["item_price"] = CanonicalNormalizer.normalize_number(
                    record["item_price"]
                )

            normalized.append(record)

        return normalized

    @staticmethod
    def normalize_number(value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            text = value.strip()

            if not text:
                return None

            try:
                number = float(text)

                if number.is_integer():
                    return int(number)

                return number
            except ValueError:
                return value

        return value

    def normalize_orders(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        output = []

        for source in records:
            record = dict(source)

            if "id" in record:
                record["id"] = self.normalize_id(record["id"])

            for field in ("created_at", "updated_at", "review_sent_at"):
                if field in record:
                    record[field] = self.normalize_timestamp(
                        record[field]
                    )

            if "order_items" in record:
                record["order_items"] = self.normalize_order_items(
                    record["order_items"]
                )

            for field in (
                "subtotal",
                "tax",
                "total",
            ):
                if field in record:
                    record[field] = self.normalize_number(
                        record[field]
                    )

            output.append(record)

        return output

    def normalize_menus(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        output = []

        for source in records:
            record = dict(source)

            if "id" in record:
                record["id"] = self.normalize_id(record["id"])

            for field in ("created_at", "updated_at"):
                if field in record:
                    record[field] = self.normalize_timestamp(
                        record[field]
                    )

            if "order_count" in record:
                record["order_count"] = self.normalize_number(
                    record["order_count"]
                )

            output.append(record)

        return output

    def normalize_stock_managements(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        output = []

        for source in records:
            record = dict(source)

            if "id" in record:
                record["id"] = self.normalize_id(record["id"])

            for field in ("created_at", "updated_at", "last_updated"):
                if field in record:
                    record[field] = self.normalize_timestamp(
                        record[field]
                    )

            if "quantity" in record:
                record["quantity"] = self.normalize_number(
                    record["quantity"]
                )

            output.append(record)

        return output

    def normalize_stock_logs(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        output = []

        for source in records:
            record = dict(source)

            if "id" in record:
                record["id"] = self.normalize_id(record["id"])

            for field in ("created_at", "updated_at"):
                if field in record:
                    record[field] = self.normalize_timestamp(
                        record[field]
                    )

            if "item" in record:
                record["item"] = self.normalize_id(record["item"])

            if "quantity" in record:
                record["quantity"] = self.normalize_number(
                    record["quantity"]
                )

            output.append(record)

        return output

    def normalize_stock_requirements(
        self,
        records: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        output = []

        for source in records:
            record = dict(source)

            if "id" in record:
                record["id"] = self.normalize_id(record["id"])

            if "item_id" in record:
                record["item_id"] = self.normalize_id(
                    record["item_id"]
                )

            for field in ("created_at", "updated_at"):
                if field in record:
                    record[field] = self.normalize_timestamp(
                        record[field]
                    )

            if "quantity" in record:
                record["quantity"] = self.normalize_number(
                    record["quantity"]
                )

            if "vendor_id" in record:
                record["vendor_id"] = self.normalize_id(
                    record["vendor_id"]
                )

            if "restaurant_id" in record:
                record["restaurant_id"] = self.normalize_id(
                    record["restaurant_id"]
                )

            output.append(record)

        return output

    def normalize_all(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "orders": self.normalize_orders(
                self.load("orders")
            ),
            "menus": self.normalize_menus(
                self.load("menus")
            ),
            "stock_managements": self.normalize_stock_managements(
                self.load("stock_managements")
            ),
            "stock_logs": self.normalize_stock_logs(
                self.load("stock_logs")
            ),
            "stock_requirements": self.normalize_stock_requirements(
                self.load("stock_requirements")
            ),
        }


def write_canonical(
    data: dict[str, list[dict[str, Any]]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for table, records in data.items():
        path = output_dir / f"{table}.json"

        with path.open("w", encoding="utf-8") as file:
            json.dump(
                records,
                file,
                indent=2,
                ensure_ascii=False,
                default=str,
            )