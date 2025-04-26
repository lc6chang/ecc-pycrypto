from __future__ import annotations
import dataclasses
import abc


@dataclasses.dataclass
class AbstractPoint(abc.ABC):
    curve: Curve

    def __neg__(self) -> AbstractPoint:
        return self.curve.neg_point(self)

    def __add__(self, other: AbstractPoint) -> AbstractPoint:
        return self.curve.add_point(self, other)

    def __radd__(self, other: AbstractPoint) -> AbstractPoint:
        return self.__add__(other)

    def __sub__(self, other: AbstractPoint) -> AbstractPoint:
        negative = -other
        return self.__add__(negative)

    def __mul__(self, scalar: int) -> AbstractPoint:
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int) -> AbstractPoint:
        return self.__mul__(scalar)


@dataclasses.dataclass
class Point(AbstractPoint):
    x: int
    y: int

    def __post_init__(self):
        if not self.curve.is_on_curve(self):
            raise ValueError(f"{self} is not on the curve.")


@dataclasses.dataclass
class InfinityPoint(AbstractPoint):
    pass


@dataclasses.dataclass
class Curve(abc.ABC):
    name: str
    a: int
    b: int
    p: int
    n: int
    G_x: int
    G_y: int

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()
