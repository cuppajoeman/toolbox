from __future__ import annotations

from dataclasses import dataclass
from math import log


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        escape_count = self.continuous_escape_count(c) if smooth else self.escape_count(c)
        value = escape_count / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def escape_count(self, c: complex) -> int:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > self.escape_radius:
                return iteration # this means unstable
        return self.max_iterations # this means stable

    def continuous_escape_count(self, c: complex) -> float:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > self.escape_radius:
                return iteration + 1 - log(log(abs(z))) / log(2)
        return self.max_iterations
