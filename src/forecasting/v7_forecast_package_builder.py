from __future__ import annotations

from datetime import date

from src.forecasting.forecast_run_result import ForecastRunResult
from src.forecasting.v7_forecast_point_builder import ForecastPointBuilder
from src.forecasting.v7_forecast_types import (
    ForecastPackage,
    ForecastSeries,
)


class ForecastPackageBuilder:
    def __init__(
        self,
        point_builder: ForecastPointBuilder | None = None,
    ) -> None:
        self.point_builder = (
            point_builder or ForecastPointBuilder()
        )

    def build(
        self,
        results: list[ForecastRunResult],
    ) -> ForecastPackage:
        if not results:
            raise ValueError("results cannot be empty")

        series: list[ForecastSeries] = []

        for result in results:
            series.append(
                self.point_builder.build(result)
            )

        start_dates = {
            result.start_date
            for result in results
        }

        horizons = {
            result.horizon
            for result in results
        }

        if len(start_dates) != 1:
            raise ValueError(
                "all results must have the same start date"
            )

        if len(horizons) != 1:
            raise ValueError(
                "all results must have the same horizon"
            )

        return ForecastPackage(
            start_date=next(iter(start_dates)),
            horizon=next(iter(horizons)),
            series=tuple(series),
        )
