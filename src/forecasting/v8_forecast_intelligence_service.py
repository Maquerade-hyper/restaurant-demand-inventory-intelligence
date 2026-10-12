from __future__ import annotations

from src.forecasting.v8_forecast_bounds import (
    ForecastBoundsBuilder,
)
from src.forecasting.v8_forecast_confidence import (
    ForecastConfidenceMetadataBuilder,
)
from src.forecasting.v8_forecast_distribution import (
    ForecastDistribution,
)
from src.forecasting.v8_forecast_intelligence import (
    ForecastIntelligence,
)
from src.forecasting.v8_forecast_risk import (
    ForecastRiskAnalyzer,
)
from src.forecasting.v8_forecast_statistics import (
    ForecastStatistics,
)
from src.forecasting.v8_forecast_uncertainty import (
    ForecastUncertaintyAnalyzer,
)
from src.forecasting.v8_forecast_variability import (
    ForecastVariabilityAnalyzer,
)


class ForecastIntelligenceService:
    def __init__(self) -> None:
        self.statistics = ForecastStatistics()
        self.variability = ForecastVariabilityAnalyzer()
        self.uncertainty = ForecastUncertaintyAnalyzer()
        self.bounds = ForecastBoundsBuilder()
        self.risks = ForecastRiskAnalyzer()
        self.confidence = (
            ForecastConfidenceMetadataBuilder()
        )

    def analyze(
        self,
        values: list[float] | tuple[float, ...],
    ) -> ForecastIntelligence:
        if not values:
            raise ValueError(
                "forecast values cannot be empty"
            )

        if any(value < 0 for value in values):
            raise ValueError(
                "forecast values cannot be negative"
            )

        distribution = ForecastDistribution(
            values=tuple(float(value) for value in values)
        )

        statistics = self.statistics.calculate(
            distribution
        )

        variability = self.variability.analyze(
            statistics
        )

        uncertainty = self.uncertainty.analyze(
            mean_value=statistics["mean"],
            standard_deviation=statistics["std"],
        )

        bounds = self.bounds.build(
            mean_value=statistics["mean"],
            standard_deviation=statistics["std"],
        )

        risks = self.risks.analyze(
            total=statistics["total"],
            coefficient_of_variation=(
                variability.coefficient_of_variation
            ),
            relative_uncertainty=(
                uncertainty.relative_uncertainty
            ),
        )

        confidence = self.confidence.build(
            observations=distribution.count,
            uncertainty_available=True,
        )

        return ForecastIntelligence(
            statistics=statistics,
            variability=variability,
            uncertainty=uncertainty,
            bounds=bounds,
            risks=risks,
            confidence=confidence,
        )
