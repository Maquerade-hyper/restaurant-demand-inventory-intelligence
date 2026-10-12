from __future__ import annotations

from datetime import date, timedelta


class ForecastDateGenerator:
    def generate(
        self,
        start_date: date,
        horizon_days: int,
    ) -> list[date]:
        if horizon_days <= 0:
            raise ValueError(
                "Forecast horizon must be greater than 0"
            )

        return [
            start_date + timedelta(days=offset)
            for offset in range(1, horizon_days + 1)
        ]