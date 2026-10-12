from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastUncertainty:
    standard_deviation: float
    relative_uncertainty: float


class ForecastUncertaintyAnalyzer:
    def analyze(
        self,
        mean_value: float,
        standard_deviation: float,
    ) -> ForecastUncertainty:
        if mean_value < 0:
            raise ValueError(
                "mean forecast cannot be negative"
            )

        if standard_deviation < 0:
            raise ValueError(
                "standard deviation cannot be negative"
            )

        if mean_value == 0:
            relative_uncertainty = 0.0
        else:
            relative_uncertainty = (
                standard_deviation / mean_value
            )

        return ForecastUncertainty(
            standard_deviation=standard_deviation,
            relative_uncertainty=relative_uncertainty,
        )
