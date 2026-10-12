from datetime import date, timedelta

from src.forecasting.future_feature_builder import (
    FutureFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 41 - FUTURE FEATURE BUILDER")
    print("=" * 70)

    builder = FutureFeatureBuilder()

    dates = [
        date(2026, 9, 1) + timedelta(days=i)
        for i in range(1, 15)
    ]

    rows = builder.build(
        dates=dates,
        restaurant=20,
        item_id=305,
    )

    print()
    print(f"Future rows:            {len(rows)}")
    print(f"Restaurant:             {rows[0].restaurant}")
    print(f"Item ID:                {rows[0].item_id}")
    print(f"First date:             {rows[0].date}")
    print(f"Last date:              {rows[-1].date}")
    print()

    assert len(rows) == 14
    assert rows[0].date == date(2026, 9, 2)
    assert rows[-1].date == date(2026, 9, 15)
    assert all(row.restaurant == 20 for row in rows)
    assert all(row.item_id == 305 for row in rows)

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()