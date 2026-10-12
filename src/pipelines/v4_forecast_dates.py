from datetime import date

from src.forecasting.forecast_dates import ForecastDateGenerator


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 38 - FORECAST DATE GENERATOR")
    print("=" * 70)

    generator = ForecastDateGenerator()

    start_date = date(2026, 9, 1)
    dates = generator.generate(
        start_date=start_date,
        horizon_days=14,
    )

    print()
    print(f"Start date:             {start_date}")
    print(f"Generated dates:        {len(dates)}")
    print(f"First forecast date:    {dates[0]}")
    print(f"Last forecast date:     {dates[-1]}")
    print()

    assert len(dates) == 14
    assert dates[0] == date(2026, 9, 2)
    assert dates[-1] == date(2026, 9, 15)

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()