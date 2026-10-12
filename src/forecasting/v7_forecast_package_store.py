from __future__ import annotations

import json
from pathlib import Path

from src.forecasting.v7_forecast_types import ForecastPackage


class ForecastPackageStore:
    def save(
        self,
        package: ForecastPackage,
        path: str | Path,
    ) -> Path:
        output_path = Path(path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "start_date": package.start_date.isoformat(),
            "horizon": package.horizon,
            "series": [
                {
                    "restaurant": series.restaurant,
                    "item_id": series.item_id,
                    "total": series.total,
                    "points": [
                        {
                            "date": point.date.isoformat(),
                            "restaurant": point.restaurant,
                            "item_id": point.item_id,
                            "prediction": point.prediction,
                        }
                        for point in series.points
                    ],
                }
                for series in package.series
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
