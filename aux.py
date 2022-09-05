from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate2D:
    x: float
    y: float
