from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastRiskSignals:
    high_variability: bool
    zero_demand: bool
    wide_uncertainty: bool


class ForecastRiskAnalyzer:
    def analyze(
        self,
        total: float,
        coefficient_of_variation: float,
        relative_uncertainty: float,
    ) -> ForecastRiskSignals:
        return ForecastRiskSignals(
            high_variability=coefficient_of_variation > 1.0,
            zero_demand=total == 0.0,
            wide_uncertainty=relative_uncertainty > 1.0,
        )
