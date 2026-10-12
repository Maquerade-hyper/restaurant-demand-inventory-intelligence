from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState
from src.forecasting.recursive_rolling_resolver import (
    RecursiveRollingResolver,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 49 - RECURSIVE ROLLING RESOLVER")
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

    resolver = RecursiveRollingResolver()

    rolling = resolver.resolve(
        forecast_date=forecast_date,
        state=state,
    )

    print()
    print(f"Forecast date:          {forecast_date}")
    print(
        f"Rolling mean 7:         "
        f"{rolling['rolling_mean_7']}"
    )
    print(
        f"Rolling mean 14:        "
        f"{rolling['rolling_mean_14']}"
    )
    print(
        f"Rolling mean 28:        "
        f"{rolling['rolling_mean_28']}"
    )
    print(
        f"Rolling max 7:          "
        f"{rolling['rolling_max_7']}"
    )
    print(
        f"Rolling std 7:          "
        f"{rolling['rolling_std_7']}"
    )
    print()

    assert rolling["rolling_mean_7"] == 4.785714285714286
    assert rolling["rolling_mean_14"] == 7.392857142857143
    assert rolling["rolling_mean_28"] == 13.946428571428571
    assert rolling["rolling_max_7"] == 12.5

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()