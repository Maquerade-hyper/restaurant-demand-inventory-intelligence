from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inventory.v10_decision_contract import (
    InventoryDecisionInput,
)
from src.inventory.v10_decision_service import (
    InventoryDecisionService,
)
from src.inventory.v10_package_store import (
    InventoryPackageJsonStore,
)


def main() -> None:

    decision_input = InventoryDecisionInput(
        item_id=305,
        restaurant=20,
        forecast_demand=18.715188293143164,
        current_stock=10.0,
        standard_deviation=0.18466185486194964,
        confirmed_incoming=2.0,
        pack_size=1.0,
        minimum_order_quantity=0.0,
    )

    service = InventoryDecisionService()

    package = service.build(
        decision_input
    )

    if not package.validation.valid:
        raise RuntimeError(
            "V10 decision validation failed: "
            + "; ".join(package.validation.errors)
        )

    output_path = (
        ROOT
        / "data"
        / "features"
        / "v10_inventory_decision.json"
    )

    store = InventoryPackageJsonStore()

    saved_path = store.save(
        package,
        output_path,
    )

    intelligence = package.intelligence

    print("=" * 62)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V10 - FINAL INVENTORY DECISION")
    print("=" * 62)

    print()
    print("IDENTITY")
    print(f"Item:                   {decision_input.item_id}")
    print(f"Restaurant:             {decision_input.restaurant}")

    print()
    print("DEMAND")
    print(
        f"Forecast demand:        "
        f"{decision_input.forecast_demand}"
    )

    print()
    print("SAFETY STOCK")
    print(
        f"Safety stock:           "
        f"{intelligence.safety_stock.safety_stock}"
    )

    print()
    print("INVENTORY")
    print(
        f"Current stock:          "
        f"{decision_input.current_stock}"
    )
    print(
        f"Confirmed incoming:     "
        f"{decision_input.confirmed_incoming}"
    )

    print()
    print("PURCHASE")
    print(
        f"Net requirement:        "
        f"{intelligence.purchase.net_requirement}"
    )
    print(
        f"Recommended quantity:   "
        f"{intelligence.purchase.recommended_quantity}"
    )
    print(
        f"Should purchase:        "
        f"{intelligence.purchase.should_purchase}"
    )

    print()
    print("RISKS")
    print(
        f"Stockout risk:          "
        f"{intelligence.stockout.risk}"
    )
    print(
        f"Excess stock risk:      "
        f"{intelligence.excess_stock.risk}"
    )

    print()
    print("ACTION")
    print(
        f"Decision:               "
        f"{package.action_plan.action}"
    )

    if package.purchase_line is not None:
        print(
            f"Purchase line quantity: "
            f"{package.purchase_line.quantity}"
        )

    print()
    print("VALIDATION")
    print(
        f"Valid:                  "
        f"{package.validation.valid}"
    )

    print()
    print("OUTPUT")
    print(f"JSON: {saved_path}")

    print()
    print("STATUS: PASSED")
    print("=" * 62)


if __name__ == "__main__":
    main()
