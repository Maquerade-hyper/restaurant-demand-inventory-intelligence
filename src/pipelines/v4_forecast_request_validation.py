from datetime import date

from src.forecasting.forecast_request import ForecastRequestBuilder
from src.forecasting.forecast_request_validator import (
    ForecastRequestValidator,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V4 PART 40 - FORECAST REQUEST VALIDATION")
    print("=" * 70)

    builder = ForecastRequestBuilder()
    validator = ForecastRequestValidator()

    request = builder.build(
        restaurant=20,
        item_id=305,
        start_date=date(2026, 9, 1),
        horizon_days=14,
    )

    validator.validate(request)

    print()
    print(f"Restaurant:             {request.restaurant}")
    print(f"Item ID:                {request.item_id}")
    print(f"Start date:             {request.start_date}")
    print(f"Horizon:                {request.horizon_days} days")
    print("Validation:             PASSED")
    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()