from __future__ import annotations

from math import sqrt


def mae(
    actual: list[float],
    predicted: list[float],
) -> float:
    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted lengths must match"
        )

    if not actual:
        return 0.0

    return sum(
        abs(a - p)
        for a, p in zip(actual, predicted)
    ) / len(actual)


def rmse(
    actual: list[float],
    predicted: list[float],
) -> float:
    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted lengths must match"
        )

    if not actual:
        return 0.0

    mse = sum(
        (a - p) ** 2
        for a, p in zip(actual, predicted)
    ) / len(actual)

    return sqrt(mse)


def smape(
    actual: list[float],
    predicted: list[float],
) -> float:
    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted lengths must match"
        )

    if not actual:
        return 0.0

    total = 0.0
    count = 0

    for a, p in zip(actual, predicted):
        denominator = abs(a) + abs(p)

        if denominator == 0:
            continue

        total += (
            2.0 * abs(a - p)
        ) / denominator

        count += 1

    if count == 0:
        return 0.0

    return (total / count) * 100.0


def evaluate(
    actual: list[float],
    predicted: list[float],
) -> dict[str, float]:
    return {
        "mae": mae(actual, predicted),
        "rmse": rmse(actual, predicted),
        "smape": smape(actual, predicted),
    }


def evaluate_segments(
    actual: list[float],
    predicted: list[float],
) -> dict[str, dict[str, float]]:
    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted lengths must match"
        )

    segments = {
        "all": (
            actual,
            predicted,
        ),
        "zero_actual": (
            [
                a
                for a in actual
                if a == 0
            ],
            [
                p
                for a, p in zip(actual, predicted)
                if a == 0
            ],
        ),
        "positive_actual": (
            [
                a
                for a in actual
                if a > 0
            ],
            [
                p
                for a, p in zip(actual, predicted)
                if a > 0
            ],
        ),
    }

    return {
        name: evaluate(
            segment_actual,
            segment_predicted,
        )
        for name, (
            segment_actual,
            segment_predicted,
        ) in segments.items()
    }


def evaluate_segments(
    actual: list[float],
    predicted: list[float],
) -> dict[str, dict[str, float]]:
    if len(actual) != len(predicted):
        raise ValueError(
            "actual and predicted lengths must match"
        )

    zero_actual = [
        (a, p)
        for a, p in zip(actual, predicted)
        if a == 0
    ]

    positive_actual = [
        (a, p)
        for a, p in zip(actual, predicted)
        if a > 0
    ]

    segments = {
        "all": (actual, predicted),
        "zero_actual": (
            [a for a, _ in zero_actual],
            [p for _, p in zero_actual],
        ),
        "positive_actual": (
            [a for a, _ in positive_actual],
            [p for _, p in positive_actual],
        ),
    }

    return {
        name: evaluate(segment_actual, segment_predicted)
        for name, (segment_actual, segment_predicted)
        in segments.items()
    }