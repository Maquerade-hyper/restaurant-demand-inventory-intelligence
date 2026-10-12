from __future__ import annotations

from pathlib import Path
import json
from typing import Any


TABLES = (
    "orders",
    "menus",
    "stock_managements",
    "stock_logs",
    "stock_requirements",
)


class CanonicalDataset:
    """
    Loads the normalized canonical dataset.

    This layer is read-only.
    It does not:
    - modify source records
    - infer missing relationships
    - merge records by name
    - create artificial demand
    """

    def __init__(self, canonical_dir: Path):
        self.canonical_dir = Path(canonical_dir)

    def _load_table(self, table: str) -> list[dict[str, Any]]:
        path = self.canonical_dir / f"{table}.json"

        if not path.exists():
            raise FileNotFoundError(
                f"Canonical table not found: {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                f"Canonical table must contain a list: {path}"
            )

        for index, row in enumerate(data):
            if not isinstance(row, dict):
                raise ValueError(
                    f"{table}[{index}] is not an object"
                )

        return data

    def load(self) -> dict[str, list[dict[str, Any]]]:
        return {
            table: self._load_table(table)
            for table in TABLES
        }

    def count(self, table: str) -> int:
        return len(self._load_table(table))

    def counts(self) -> dict[str, int]:
        return {
            table: self.count(table)
            for table in TABLES
        }

    def table(self, table: str) -> list[dict[str, Any]]:
        if table not in TABLES:
            raise KeyError(
                f"Unknown canonical table: {table}"
            )

        return self._load_table(table)