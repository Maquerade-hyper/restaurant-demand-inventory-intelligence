from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastHorizon:
    days: int


class ForecastHorizonBuilder:
    def build(self, days: int) -> ForecastHorizon:
        if days <= 0:
            raise ValueError(
                "Forecast horizon must be greater than 0"
            )

        return ForecastHorizon(days=days)