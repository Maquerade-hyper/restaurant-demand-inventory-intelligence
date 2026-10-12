from __future__ import annotations

import json
from pathlib import Path

from src.forecasting.v8_forecast_intelligence import (
    ForecastIntelligence,
)


class ForecastIntelligenceStore:
    def save(
        self,
        intelligence: ForecastIntelligence,
        path: str | Path,
    ) -> Path:
        output_path = Path(path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "statistics": intelligence.statistics,
            "variability": {
                "standard_deviation":
                    intelligence.variability.standard_deviation,
                "coefficient_of_variation":
                    intelligence.variability.coefficient_of_variation,
            },
            "uncertainty": {
                "standard_deviation":
                    intelligence.uncertainty.standard_deviation,
                "relative_uncertainty":
                    intelligence.uncertainty.relative_uncertainty,
            },
            "bounds": {
                "lower": intelligence.bounds.lower,
                "upper": intelligence.bounds.upper,
            },
            "risks": {
                "high_variability":
                    intelligence.risks.high_variability,
                "zero_demand":
                    intelligence.risks.zero_demand,
                "wide_uncertainty":
                    intelligence.risks.wide_uncertainty,
            },
            "confidence": {
                "method":
                    intelligence.confidence.method,
                "observations":
                    intelligence.confidence.observations,
                "uncertainty_available":
                    intelligence.confidence.uncertainty_available,
            },
        }

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output_path
