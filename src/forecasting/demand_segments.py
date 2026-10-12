from typing import Any


def classify_demand_series(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Classify one restaurant/item demand series.

    Classification is based only on the observed training history.
    """

    if not rows:
        return {
            "total_days": 0,
            "active_days": 0,
            "zero_days": 0,
            "total_demand": 0.0,
            "activity_ratio": 0.0,
            "zero_ratio": 0.0,
            "classification": "no_history",
        }

    demands = [
        float(row["demand_quantity"])
        for row in rows
    ]

    total_days = len(demands)

    active_days = sum(
        1
        for demand in demands
        if demand > 0
    )

    zero_days = total_days - active_days

    total_demand = sum(demands)

    activity_ratio = (
        active_days / total_days
        if total_days > 0
        else 0.0
    )

    zero_ratio = (
        zero_days / total_days
        if total_days > 0
        else 0.0
    )

    if active_days == 0:
        classification = "no_demand"

    elif activity_ratio >= 0.50:
        classification = "frequent"

    elif activity_ratio >= 0.20:
        classification = "intermittent"

    else:
        classification = "sparse"

    return {
        "total_days": total_days,
        "active_days": active_days,
        "zero_days": zero_days,
        "total_demand": total_demand,
        "activity_ratio": activity_ratio,
        "zero_ratio": zero_ratio,
        "classification": classification,
    }


def build_demand_segments(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Build demand-activity profiles for every
    restaurant/item series.
    """

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

    segments: list[dict[str, Any]] = []

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
        profile = classify_demand_series(
            series_rows
        )

        segments.append(
            {
                "restaurant": restaurant,
                "item_id": item_id,
                **profile,
            }
        )

    return segments