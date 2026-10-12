from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class ForecastState:
    demand: dict[date, float]

    def get_demand(self, target_date: date) -> float:
        if target_date not in self.demand:
            raise KeyError(
                f"No demand available for {target_date}"
            )

        return self.demand[target_date]

    def add_prediction(
        self,
        target_date: date,
        prediction: float,
    ) -> None:
        if prediction < 0:
            raise ValueError(
                "Prediction cannot be negative"
            )

        if target_date in self.demand:
            raise ValueError(
                f"Demand already exists for {target_date}"
            )

        self.demand[target_date] = prediction