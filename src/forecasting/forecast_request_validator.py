from __future__ import annotations

from datetime import date

from src.forecasting.forecast_request import ForecastRequest


class ForecastRequestValidator:
    def validate(self, request: ForecastRequest) -> None:
        if request.restaurant <= 0:
            raise ValueError(
                "Restaurant ID must be greater than 0"
            )

        if request.item_id <= 0:
            raise ValueError(
                "Item ID must be greater than 0"
            )

        if not isinstance(request.start_date, date):
            raise TypeError(
                "Start date must be a date"
            )

        if request.horizon_days <= 0:
            raise ValueError(
                "Forecast horizon must be greater than 0"
            )