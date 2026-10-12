from __future__ import annotations

from typing import Any


class NaiveForecast:
    """Forecast using the most recent observed demand."""

    def predict(
        self,
        history: list[float],
        horizon: int,
    ) -> list[float]:
        if not history:
            return [0.0] * horizon

        return [float(history[-1])] * horizon


class SeasonalNaive7:
    """Forecast using demand from 7 observations earlier."""

    def predict(
        self,
        history: list[float],
        horizon: int,
    ) -> list[float]:
        if len(history) < 7:
            return [0.0] * horizon

        value = float(history[-7])

        return [value] * horizon


class MovingAverage7:
    """Forecast using the mean of the previous 7 observations."""

    def predict(
        self,
        history: list[float],
        horizon: int,
    ) -> list[float]:
        if not history:
            return [0.0] * horizon

        window = history[-7:]

        average = sum(window) / len(window)

        return [float(average)] * horizon


def build_baseline_forecasts(
    history: list[float],
    horizon: int,
) -> dict[str, list[float]]:
    return {
        "naive": NaiveForecast().predict(
            history,
            horizon,
        ),
        "seasonal_naive_7": SeasonalNaive7().predict(
            history,
            horizon,
        ),
        "moving_average_7": MovingAverage7().predict(
            history,
            horizon,
        ),
    }