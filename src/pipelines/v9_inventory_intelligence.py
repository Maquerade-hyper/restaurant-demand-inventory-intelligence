from src.inventory.v9_inventory_intelligence import (
    InventoryIntelligenceService,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V9 - INVENTORY INTELLIGENCE")
    print("=" * 70)

    service = InventoryIntelligenceService()

    forecast_demand = 18.715188293143164
    standard_deviation = 0.18466185486194964

    result = service.analyze(
        forecast_demand=forecast_demand,
        current_stock=10.0,
        standard_deviation=standard_deviation,
        confirmed_incoming=2.0,
        pack_size=1.0,
        minimum_order_quantity=0.0,
    )

    print()
    print("DEMAND")
    print(
        f"Forecast demand:       "
        f"{forecast_demand}"
    )

    print()
    print("SAFETY STOCK")
    print(
        f"Safety stock:           "
        f"{result.safety_stock.safety_stock}"
    )
    print(
        f"Method:                 "
        f"{result.safety_stock.method}"
    )

    print()
    print("PURCHASE")
    print(
        f"Net requirement:        "
        f"{result.purchase.net_requirement}"
    )
    print(
        f"Recommended quantity:   "
        f"{result.purchase.recommended_quantity}"
    )
    print(
        f"Should purchase:        "
        f"{result.purchase.should_purchase}"
    )

    print()
    print("STOCKOUT RISK")
    print(
        f"Risk:                   "
        f"{result.stockout.risk}"
    )
    print(
        f"Available quantity:     "
        f"{result.stockout.available_quantity}"
    )

    print()
    print("EXCESS STOCK RISK")
    print(
        f"Risk:                   "
        f"{result.excess_stock.risk}"
    )
    print(
        f"Excess quantity:        "
        f"{result.excess_stock.excess_quantity}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()
