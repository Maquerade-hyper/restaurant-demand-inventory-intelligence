from __future__ import annotations

import json
from pathlib import Path

from src.forecasting.forecast_run_result import ForecastRunResult


class ForecastRunJsonStore:
    def save(
        self,
        result: ForecastRunResult,
        path: str | Path,
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "restaurant": result.restaurant,
            "item_id": result.item_id,
            "start_date": result.start_date.isoformat(),
            "horizon": result.horizon,
            "total_prediction": result.total_prediction,
            "predictions": [
                {
                    "date": prediction.date.isoformat(),
                    "restaurant": prediction.restaurant,
                    "item_id": prediction.item_id,
                    "prediction": prediction.prediction,
                }
                for prediction in result.predictions
            ],
        }

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output_path
