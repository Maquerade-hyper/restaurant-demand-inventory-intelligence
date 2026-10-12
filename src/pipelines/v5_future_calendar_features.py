from datetime import date

from src.forecasting.future_calendar_features import (
    FutureCalendarFeatureBuilder,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 42 - FUTURE CALENDAR FEATURES")
    print("=" * 70)

    builder = FutureCalendarFeatureBuilder()

    forecast_date = date(2026, 9, 5)

    features = builder.build(forecast_date)

    print()
    print(f"Date:                   {features.date}")
    print(f"Day of week:            {features.day_of_week}")
    print(f"Day of month:           {features.day_of_month}")
    print(f"Month:                  {features.month}")
    print(f"Is weekend:             {features.is_weekend}")
    print()

    assert features.date == date(2026, 9, 5)
    assert features.day_of_week == 5
    assert features.day_of_month == 5
    assert features.month == 9
    assert features.is_weekend == 1

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()