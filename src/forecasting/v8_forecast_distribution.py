from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastDistribution:
    values: tuple[float, ...]

    @property
    def count(self) -> int:
        return len(self.values)

    @property
    def total(self) -> float:
        return sum(self.values)

    @property
    def minimum(self) -> float:
        if not self.values:
            raise ValueError("forecast distribution cannot be empty")
        return min(self.values)

    @property
    def maximum(self) -> float:
        if not self.values:
            raise ValueError("forecast distribution cannot be empty")
        return max(self.values)
