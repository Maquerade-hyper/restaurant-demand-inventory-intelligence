from typing import Any


def calculate_sparse_diagnostics(
    rows: list[dict[str, Any]],
) -> dict[str, float]:
    if not rows:
        return {
            "total_days": 0,
            "active_days": 0,
            "zero_days": 0,
            "total_demand": 0.0,
            "mean_demand": 0.0,
            "mean_active_demand": 0.0,
            "max_demand": 0.0,
            "demand_frequency": 0.0,
            "zero_ratio": 0.0,
        }

    demands = [
        float(row["demand_quantity"])
        for row in rows
    ]

    total_days = len(demands)

    active = [
        demand
        for demand in demands
        if demand > 0
    ]

    active_days = len(active)
    zero_days = total_days - active_days

    total_demand = sum(demands)

    mean_demand = (
        total_demand / total_days
        if total_days
        else 0.0
    )

    mean_active_demand = (
        sum(active) / active_days
        if active_days
        else 0.0
    )

    max_demand = (
        max(demands)
        if demands
        else 0.0
    )

    demand_frequency = (
        active_days / total_days
        if total_days
        else 0.0
    )

    zero_ratio = (
        zero_days / total_days
        if total_days
        else 0.0
    )

    return {
        "total_days": total_days,
        "active_days": active_days,
        "zero_days": zero_days,
        "total_demand": total_demand,
        "mean_demand": mean_demand,
        "mean_active_demand": mean_active_demand,
        "max_demand": max_demand,
        "demand_frequency": demand_frequency,
        "zero_ratio": zero_ratio,
    }


def build_sparse_diagnostics(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[
        tuple[Any, Any],
        list[dict[str, Any]],
    ] = {}

    for row in rows:
        key = (
            row.get("restaurant"),
            row.get("item_id"),
        )

        grouped.setdefault(
            key,
            [],
        ).append(row)

    results: list[dict[str, Any]] = []

    for (
        restaurant,
        item_id,
    ), series_rows in sorted(
        grouped.items(),
        key=lambda pair: (
            str(pair[0][0]),
            str(pair[0][1]),
        ),
    ):
        diagnostics = calculate_sparse_diagnostics(
            series_rows
        )

        results.append(
            {
                "restaurant": restaurant,
                "item_id": item_id,
                **diagnostics,
            }
        )

    return results