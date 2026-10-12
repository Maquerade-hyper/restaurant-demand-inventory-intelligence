from __future__ import annotations

from src.forecasting.forecast_run_result import ForecastRunResult
from src.forecasting.v7_forecast_diagnostics import (
    ForecastDiagnostics,
    ForecastDiagnosticsBuilder,
)
from src.forecasting.v7_forecast_horizon_summary import (
    ForecastHorizonSummary,
    ForecastHorizonSummarizer,
)
from src.forecasting.v7_forecast_package_builder import (
    ForecastPackageBuilder,
)
from src.forecasting.v7_forecast_types import (
    ForecastPackage,
    ForecastSeries,
)


class ForecastProcessingService:
    def __init__(self) -> None:
        self.package_builder = ForecastPackageBuilder()
        self.summary_builder = ForecastHorizonSummarizer()
        self.diagnostics_builder = ForecastDiagnosticsBuilder()

    def process(
        self,
        results: list[ForecastRunResult],
    ) -> ForecastPackage:
        return self.package_builder.build(results)

    def summarize(
        self,
        series: ForecastSeries,
    ) -> ForecastHorizonSummary:
        return self.summary_builder.summarize(series)

    def diagnostics(
        self,
        series: ForecastSeries,
    ) -> ForecastDiagnostics:
        return self.diagnostics_builder.build(series)
