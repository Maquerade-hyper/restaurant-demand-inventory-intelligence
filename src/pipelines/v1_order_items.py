from __future__ import annotations

import json
from pathlib import Path

from src.dataset.canonical_dataset import CanonicalDataset
from src.features.order_items import OrderItemDatasetBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_DIR = PROJECT_ROOT / "data" / "canonical"
FEATURE_DIR = PROJECT_ROOT / "data" / "features"

OUTPUT_FILE = FEATURE_DIR / "order_items.json"


def main() -> None:
    dataset = CanonicalDataset(CANONICAL_DIR)

    orders = dataset.table("orders")

    builder = OrderItemDatasetBuilder(orders)

    records = builder.build()

    FEATURE_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 ORDER-ITEM DATASET")
    print("=" * 70)

    print(f"Orders processed:       {len(orders)}")
    print(f"Order-item rows:        {len(records)}")
    print(f"Output:                 {OUTPUT_FILE}")

    if not records:
        raise RuntimeError(
            "Order-item dataset is empty"
        )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()