from typing import Any


def aggregate_rolling_results(
    rolling_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Aggregate metrics across rolling windows.

    No model ranking or winner selection is performed.
    """

    grouped: dict[
        tuple[str, str],
        list[dict[str, float]],
    ] = {}

    for window in rolling_results:
        for source_name in (
            "baseline_results",
            "intermittent_results",
        ):
            model_results = window.get(
                source_name,
                {},
            )

            for model_name, segments in (
                model_results.items()
            ):
                for segment_name, metrics in (
                    segments.items()
                ):
                    key = (
                        model_name,
                        segment_name,
                    )

                    grouped.setdefault(
                        key,
                        [],
                    ).append(metrics)

    aggregated: list[dict[str, Any]] = []

    for (
        model_name,
        segment_name,
    ), metric_values in sorted(
        grouped.items()
    ):
        count = len(metric_values)

        aggregated.append(
            {
                "model": model_name,
                "segment": segment_name,
                "windows": count,
                "mae_mean": sum(
                    item["mae"]
                    for item in metric_values
                ) / count,
                "mae_min": min(
                    item["mae"]
                    for item in metric_values
                ),
                "mae_max": max(
                    item["mae"]
                    for item in metric_values
                ),
                "rmse_mean": sum(
                    item["rmse"]
                    for item in metric_values
                ) / count,
                "rmse_min": min(
                    item["rmse"]
                    for item in metric_values
                ),
                "rmse_max": max(
                    item["rmse"]
                    for item in metric_values
                ),
                "smape_mean": sum(
                    item["smape"]
                    for item in metric_values
                ) / count,
                "smape_min": min(
                    item["smape"]
                    for item in metric_values
                ),
                "smape_max": max(
                    item["smape"]
                    for item in metric_values
                ),
            }
        )

    return aggregated