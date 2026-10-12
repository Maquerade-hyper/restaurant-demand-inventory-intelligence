from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastBounds:
    lower: float
    upper: float


class ForecastBoundsBuilder:
    def build(
        self,
        mean_value: float,
        standard_deviation: float,
        multiplier: float = 1.96,
    ) -> ForecastBounds:
        if standard_deviation < 0:
            raise ValueError(
                "standard deviation cannot be negative"
            )

        if multiplier < 0:
            raise ValueError(
                "multiplier cannot be negative"
            )

        lower = max(
            0.0,
            mean_value - multiplier * standard_deviation,
        )

        upper = max(
            lower,
            mean_value + multiplier * standard_deviation,
        )

        return ForecastBounds(
            lower=lower,
            upper=upper,
        )
