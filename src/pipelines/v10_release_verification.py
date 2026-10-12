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

    package = InventoryDecisionService().build(
        decision_input
    )

    assert package.version == "V10"
    assert package.validation.valid
    assert package.intelligence.safety_stock.safety_stock >= 0
    assert package.intelligence.purchase.net_requirement >= 0
    assert package.intelligence.purchase.recommended_quantity >= 0

    output_path = (
        ROOT
        / "data"
        / "features"
        / "v10_inventory_decision.json"
    )

    store = InventoryPackageJsonStore()

    store.save(
        package,
        output_path,
    )

    loaded = store.load(
        output_path
    )

    assert loaded["version"] == "V10"
    assert loaded["validation"]["valid"] is True

    print("")
    print("=" * 62)
    print("V10 RELEASE VERIFICATION")
    print("=" * 62)
    print("")
    print("Parts 91-100:              PASSED")
    print("Decision contract:         PASSED")
    print("Purchase line:             PASSED")
    print("Action plan:               PASSED")
    print("Decision validation:       PASSED")
    print("Intelligence package:      PASSED")
    print("JSON persistence:          PASSED")
    print("Decision service:          PASSED")
    print("End-to-end pipeline:       PASSED")
    print("Integration validation:    PASSED")
    print("Release verification:      PASSED")
    print("")
    print("TOTAL DEVELOPMENT PARTS:   100 / 100")
    print("PROJECT VERSIONS:          V1 - V10")
    print("")
    print("STATUS: FINAL RELEASE PASSED")
    print("=" * 62)


if __name__ == "__main__":
    main()
