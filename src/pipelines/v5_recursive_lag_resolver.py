from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState
from src.forecasting.recursive_lag_resolver import (
    RecursiveLagResolver,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 48 - RECURSIVE LAG RESOLVER")
    print("=" * 70)

    forecast_start = date(2026, 9, 1)

    history = {
        forecast_start - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    state = ForecastState(
        demand=history.copy()
    )

    state.add_prediction(
        forecast_start,
        12.5,
    )

    forecast_date = date(2026, 9, 2)

    resolver = RecursiveLagResolver()

    lags = resolver.resolve(
        forecast_date=forecast_date,
        state=state,
    )

    print()
    print(f"Forecast date:          {forecast_date}")
    print(f"Lag 1:                  {lags['lag_1']}")
    print(f"Lag 7:                  {lags['lag_7']}")
    print(f"Lag 14:                 {lags['lag_14']}")
    print(f"Lag 28:                 {lags['lag_28']}")
    print()

    assert lags["lag_1"] == 12.5
    assert lags["lag_7"] == 6.0
    assert lags["lag_14"] == 13.0
    assert lags["lag_28"] == 27.0

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()