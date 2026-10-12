from __future__ import annotations

from dataclasses import dataclass

from src.forecasting.v8_forecast_bounds import ForecastBounds
from src.forecasting.v8_forecast_confidence import (
    ForecastConfidenceMetadata,
)
from src.forecasting.v8_forecast_risk import ForecastRiskSignals
from src.forecasting.v8_forecast_uncertainty import (
    ForecastUncertainty,
)
from src.forecasting.v8_forecast_variability import (
    ForecastVariability,
)


@dataclass(frozen=True)
class ForecastIntelligence:
    statistics: dict[str, float]
    variability: ForecastVariability
    uncertainty: ForecastUncertainty
    bounds: ForecastBounds
    risks: ForecastRiskSignals
    confidence: ForecastConfidenceMetadata
