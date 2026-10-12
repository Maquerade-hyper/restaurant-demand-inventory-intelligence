from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastConfidenceMetadata:
    method: str
    observations: int
    uncertainty_available: bool


class ForecastConfidenceMetadataBuilder:
    def build(
        self,
        observations: int,
        uncertainty_available: bool,
    ) -> ForecastConfidenceMetadata:
        if observations < 0:
            raise ValueError(
                "observations cannot be negative"
            )

        return ForecastConfidenceMetadata(
            method="empirical_forecast_variability",
            observations=observations,
            uncertainty_available=uncertainty_available,
        )
