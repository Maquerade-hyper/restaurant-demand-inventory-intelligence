from datetime import date, timedelta

from src.forecasting.forecast_state import ForecastState


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V5 PART 47 - FORECAST STATE")
    print("=" * 70)

    start_date = date(2026, 9, 1)

    history = {
        start_date - timedelta(days=days): float(days)
        for days in range(1, 29)
    }

    state = ForecastState(
        demand=history.copy()
    )

    forecast_date = start_date

    state.add_prediction(
        target_date=forecast_date,
        prediction=12.5,
    )

    print()
    print(f"Historical entries:     {len(history)}")
    print(
        f"Prediction date:        {forecast_date}"
    )
    print(
        f"Prediction:             "
        f"{state.get_demand(forecast_date)}"
    )
    print(
        f"Total state entries:    "
        f"{len(state.demand)}"
    )
    print()

    assert len(history) == 28
    assert len(state.demand) == 29
    assert state.get_demand(forecast_date) == 12.5

    print("STATUS: PASSED")


if __name__ == "__main__":
    main()