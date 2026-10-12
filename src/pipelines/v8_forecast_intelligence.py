from src.forecasting.v8_forecast_intelligence_service import (
    ForecastIntelligenceService,
)
from src.forecasting.v8_forecast_intelligence_store import (
    ForecastIntelligenceStore,
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V8 - FORECAST INTELLIGENCE")
    print("=" * 70)

    values = (
        2.5,
        2.928571428571429,
        2.923469387755102,
        2.7725947521865892,
        2.6094856309870886,
        2.5000371868864164,
        2.4810299067565387,
    )

    service = ForecastIntelligenceService()

    intelligence = service.analyze(values)

    output = ForecastIntelligenceStore().save(
        intelligence,
        "data/features/v8_forecast_intelligence.json",
    )

    print()
    print("STATISTICS")
    print(
        f"Mean:                  "
        f"{intelligence.statistics['mean']}"
    )
    print(
        f"Median:                "
        f"{intelligence.statistics['median']}"
    )
    print(
        f"Std:                   "
        f"{intelligence.statistics['std']}"
    )
    print(
        f"Minimum:               "
        f"{intelligence.statistics['minimum']}"
    )
    print(
        f"Maximum:               "
        f"{intelligence.statistics['maximum']}"
    )
    print(
        f"Total:                 "
        f"{intelligence.statistics['total']}"
    )

    print()
    print("VARIABILITY")
    print(
        f"Coefficient variation: "
        f"{intelligence.variability.coefficient_of_variation}"
    )

    print()
    print("UNCERTAINTY")
    print(
        f"Relative uncertainty:  "
        f"{intelligence.uncertainty.relative_uncertainty}"
    )

    print()
    print("BOUNDS")
    print(
        f"Lower:                 "
        f"{intelligence.bounds.lower}"
    )
    print(
        f"Upper:                 "
        f"{intelligence.bounds.upper}"
    )

    print()
    print("RISK SIGNALS")
    print(
        f"High variability:      "
        f"{intelligence.risks.high_variability}"
    )
    print(
        f"Zero demand:           "
        f"{intelligence.risks.zero_demand}"
    )
    print(
        f"Wide uncertainty:      "
        f"{intelligence.risks.wide_uncertainty}"
    )

    print()
    print("CONFIDENCE METADATA")
    print(
        f"Method:                "
        f"{intelligence.confidence.method}"
    )
    print(
        f"Observations:          "
        f"{intelligence.confidence.observations}"
    )
    print(
        f"Uncertainty available: "
        f"{intelligence.confidence.uncertainty_available}"
    )

    print()
    print(f"Output:                {output}")
    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()
