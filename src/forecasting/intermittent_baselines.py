from typing import Any


def croston_forecast(
    history: list[float],
    horizon: int,
) -> list[float]:
    if horizon <= 0:
        return []

    if not history:
        return [0.0] * horizon

    demand = [
        float(value)
        for value in history
    ]

    non_zero = [
        value
        for value in demand
        if value > 0
    ]

    if not non_zero:
        return [0.0] * horizon

    first_index = next(
        index
        for index, value in enumerate(demand)
        if value > 0
    )

    q = demand[first_index]
    interval = float(first_index + 1)

    forecast = q / interval

    return [forecast] * horizon


def sba_croston_forecast(
    history: list[float],
    horizon: int,
) -> list[float]:
    if horizon <= 0:
        return []

    if not history:
        return [0.0] * horizon

    demand = [
        float(value)
        for value in history
    ]

    non_zero = [
        value
        for value in demand
        if value > 0
    ]

    if not non_zero:
        return [0.0] * horizon

    first_index = next(
        index
        for index, value in enumerate(demand)
        if value > 0
    )

    q = demand[first_index]
    interval = float(first_index + 1)

    forecast = (
        0.5 * q / interval
    )

    return [forecast] * horizon


def build_intermittent_forecasts(
    history: list[float],
    horizon: int,
) -> dict[str, list[float]]:
    return {
        "croston": croston_forecast(
            history,
            horizon,
        ),
        "sba_croston": sba_croston_forecast(
            history,
            horizon,
        ),
    }