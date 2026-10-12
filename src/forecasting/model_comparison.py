from typing import Any


def build_model_comparison(
    baseline_results: dict[
        str,
        dict[str, dict[str, float]],
    ],
    intermittent_results: dict[
        str,
        dict[str, dict[str, float]],
    ],
) -> list[dict[str, Any]]:
    """
    Combine baseline and intermittent model results
    into one flat comparison table.

    No ranking or winner selection is performed here.
    """

    combined = {}

    for model_name, segments in baseline_results.items():
        combined[model_name] = segments

    for model_name, segments in intermittent_results.items():
        combined[model_name] = segments

    comparison: list[dict[str, Any]] = []

    for model_name, segments in combined.items():
        for segment_name, metrics in segments.items():
            comparison.append(
                {
                    "model": model_name,
                    "segment": segment_name,
                    "mae": float(metrics["mae"]),
                    "rmse": float(metrics["rmse"]),
                    "smape": float(metrics["smape"]),
                }
            )

    comparison.sort(
        key=lambda row: (
            row["segment"],
            row["model"],
        )
    )

    return comparison