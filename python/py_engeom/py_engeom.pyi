from __future__ import annotations
from typing import Any, List, Tuple, Union
from enum import Enum


class DeviationMode(Enum):
    Absolute=0
    Normal=1


class Plane:
    def __init__(self, a: float, b: float, c: float, d: float):
        ...


class Mesh:
    def __init__(self,
                 vertices: List[Tuple[float, float, float]],
                 faces: List[Tuple[int, int, int]]):
        ...

    def vertices(self) -> List[Tuple[float, float, float]]:
        ...

    def triangles(self) -> List[Tuple[int, int, int]]:
        ...

    def split(self, plane: Plane) -> Tuple[Mesh | None, Mesh | None]:
        ...

    def deviation(self, points: List[Tuple[float, float, float]], mode: DeviationMode) -> List[float]:
        ...
