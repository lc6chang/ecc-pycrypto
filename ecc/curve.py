from __future__ import annotations
import dataclasses
import abc
import os

from ecc import math_utils


@dataclasses.dataclass(frozen=True)
class Point(abc.ABC):
    curve: Curve

    def __neg__(self):
        return self.curve.neg_point(self)

    def __add__(self, other):
        if self.curve != other.curve:
            raise ValueError(f"{self} and {other} are on the different curves.")
        return self.curve.add_point(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        negative = -other
        return self.__add__(negative)

    def __mul__(self, scalar: int):
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)


@dataclasses.dataclass(frozen=True)
class AffinePoint(Point):
    x: int
    y: int

    def __post_init__(self):
        if not self.curve.is_on_curve(self.x, self.y):
            raise ValueError(f"{self} is not on the curve.")


@dataclasses.dataclass(frozen=True)
class InfinityPoint(Point):
    pass


@dataclasses.dataclass(frozen=True)
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

    @property
    def G(self) -> AffinePoint:
        return AffinePoint(self, self.G_x, self.G_y)

    def add_point(self, P: Point, Q: Point) -> Point:
        if P == self.O:
            return Q
        if Q == self.O:
            return P
        if P == -Q:
            return self.O
        assert isinstance(P, AffinePoint) and isinstance(Q, AffinePoint)
        if P == Q:
            return self._double_affine_point(P)
        return self._add_affine_point(P, Q)

    def mul_point(self, d: int, P: Point) -> Point:
        """
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if P == self.O:
            return self.O
        if d == 0:
            return self.O

        res: Point = self.O
        is_negative_scalar = d < 0
        d = -d if is_negative_scalar else d
        tmp = P
        while d:
            if d & 0x1 == 1:
                res = self.add_point(res, tmp)
            tmp = self.add_point(tmp, tmp)
            d >>= 1
        if is_negative_scalar:
            return -res
        else:
            return res

    def neg_point(self, P: Point) -> Point:
        if P == self.O:
            return self.O
        assert isinstance(P, AffinePoint)
        return self._neg_affine_point(P)

    @property
    @abc.abstractmethod
    def O(self) -> Point:  # noqa: E743
        """
        The neutral element.
        """
        pass

    @abc.abstractmethod
    def is_on_curve(self, x: int, y: int) -> bool:
        pass

    @abc.abstractmethod
    def compute_y(self, x: int) -> int | None:
        pass

    @abc.abstractmethod
    def _add_affine_point(self, P: AffinePoint, Q: AffinePoint) -> AffinePoint:
        pass

    @abc.abstractmethod
    def _double_affine_point(self, P: AffinePoint) -> AffinePoint:
        pass

    @abc.abstractmethod
    def _neg_affine_point(self, P: AffinePoint) -> AffinePoint:
        pass


@dataclasses.dataclass(frozen=True, repr=False)
class ShortWeierstrassCurve(Curve):
    """
    y^2 = x^3 + a*x + b
    https://en.wikipedia.org/wiki/Elliptic_curve
    """

    @property
    def O(self) -> Point:  # noqa: E743
        return InfinityPoint(self)

    def is_on_curve(self, x: int, y: int) -> bool:
        left = y * y
        right = (x * x * x) + (self.a * x) + self.b
        return (left - right) % self.p == 0

    def compute_y(self, x) -> int | None:
        right = (x * x * x + self.a * x + self.b) % self.p
        y = math_utils.modsqrt(right, self.p)
        return y

    def _add_affine_point(self, P: AffinePoint, Q: AffinePoint) -> AffinePoint:
        # s = (yP - yQ) / (xP - xQ)
        # xR = s^2 - xP - xQ
        # yR = yP + s * (xR - xP)
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * math_utils.modinv(delta_x, self.p)
        res_x = (s * s - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -AffinePoint(self, res_x, res_y)

    def _double_affine_point(self, P: AffinePoint) -> AffinePoint:
        # s = (3 * xP^2 + a) / (2 * yP)
        # xR = s^2 - 2 * xP
        # yR = yP + s * (xR - xP)
        s = (3 * P.x * P.x + self.a) * math_utils.modinv(2 * P.y, self.p)
        res_x = (s * s - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -AffinePoint(self, res_x, res_y)

    def _neg_affine_point(self, P: AffinePoint) -> AffinePoint:
        return AffinePoint(self, P.x, -P.y % self.p)


@dataclasses.dataclass(frozen=True, repr=False)
class MontgomeryCurve(Curve):
    """
    by^2 = x^3 + ax^2 + x
    https://en.wikipedia.org/wiki/Montgomery_curve
    """

    @property
    def O(self) -> Point:  # noqa: E743
        return InfinityPoint(self)

    def is_on_curve(self, x: int, y: int) -> bool:
        left = self.b * y * y
        right = (x * x * x) + (self.a * x * x) + x
        return (left - right) % self.p == 0

    def compute_y(self, x: int) -> int | None:
        right = (x * x * x + self.a * x * x + x) % self.p
        inv_b = math_utils.modinv(self.b, self.p)
        right = (right * inv_b) % self.p
        y = math_utils.modsqrt(right, self.p)
        return y

    def _add_affine_point(self, P: AffinePoint, Q: AffinePoint) -> AffinePoint:
        # s = (yP - yQ) / (xP - xQ)
        # xR = b * s^2 - a - xP - xQ
        # yR = yP + s * (xR - xP)
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * math_utils.modinv(delta_x, self.p)
        res_x = (self.b * s * s - self.a - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -AffinePoint(self, res_x, res_y)

    def _double_affine_point(self, P: AffinePoint) -> AffinePoint:
        # s = (3 * xP^2 + 2 * a * xP + 1) / (2 * b * yP)
        # xR = b * s^2 - a - 2 * xP
        # yR = yP + s * (xR - xP)
        up = 3 * P.x * P.x + 2 * self.a * P.x + 1
        down = 2 * self.b * P.y
        s = up * math_utils.modinv(down, self.p)
        res_x = (self.b * s * s - self.a - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return -AffinePoint(self, res_x, res_y)

    def _neg_affine_point(self, P: AffinePoint) -> AffinePoint:
        return AffinePoint(self, P.x, -P.y % self.p)


@dataclasses.dataclass(frozen=True, repr=False)
class TwistedEdwardsCurve(Curve):
    """
    ax^2 + y^2 = 1 + bx^2y^2
    https://en.wikipedia.org/wiki/Twisted_Edwards_curve
    """

    @property
    def O(self) -> Point:  # noqa: E743
        return AffinePoint(self, 0, 1)

    def is_on_curve(self, x: int, y: int) -> bool:
        left = self.a * x * x + y * y
        right = 1 + self.b * x * x * y * y
        return (left - right) % self.p == 0

    def compute_y(self, x: int) -> int | None:
        # (bx^2 - 1) * y^2 = ax^2 - 1
        right = self.a * x * x - 1
        left_scale = (self.b * x * x - 1) % self.p
        inv_scale = math_utils.modinv(left_scale, self.p)
        right = (right * inv_scale) % self.p
        y = math_utils.modsqrt(right, self.p)
        return y

    def _add_affine_point(self, P: AffinePoint, Q: AffinePoint) -> AffinePoint:
        # xR = (xP * yQ + yP * xQ) / (1 + b * xP * xQ * yP * yQ)
        up_x = P.x * Q.y + P.y * Q.x
        down_x = 1 + self.b * P.x * Q.x * P.y * Q.y
        res_x = (up_x * math_utils.modinv(down_x, self.p)) % self.p
        # yR = (yP * yQ - a * xP * xQ) / (1 - b * xP * xQ * yP * yQ)
        up_y = P.y * Q.y - self.a * P.x * Q.x
        down_y = 1 - self.b * P.x * Q.x * P.y * Q.y
        res_y = (up_y * math_utils.modinv(down_y, self.p)) % self.p
        return AffinePoint(self, res_x, res_y)

    def _double_affine_point(self, P: AffinePoint) -> AffinePoint:
        # xR = (2 * xP * yP) / (a * xP^2 + yP^2)
        up_x = 2 * P.x * P.y
        down_x = self.a * P.x * P.x + P.y * P.y
        res_x = (up_x * math_utils.modinv(down_x, self.p)) % self.p
        # yR = (yP^2 - a * xP * xP) / (2 - a * xP^2 - yP^2)
        up_y = P.y * P.y - self.a * P.x * P.x
        down_y = 2 - self.a * P.x * P.x - P.y * P.y
        res_y = (up_y * math_utils.modinv(down_y, self.p)) % self.p
        return AffinePoint(self, res_x, res_y)

    def _neg_affine_point(self, P: AffinePoint) -> AffinePoint:
        return AffinePoint(self, -P.x % self.p, P.y)


def encode(plaintext: bytes, curve: Curve) -> AffinePoint:
    # Here we assume the length can be represented in one byte.
    byte_len = len(plaintext).to_bytes(1, "little")
    plaintext = byte_len + plaintext
    while True:
        x = int.from_bytes(plaintext, "little")
        y = curve.compute_y(x)
        if y is not None:
            return AffinePoint(curve, x, y)
        plaintext += os.urandom(1)


def decode(M: AffinePoint) -> bytes:
    byte_len = M.x & 0xff
    plaintext_int = (M.x >> 8) & (2**(byte_len * 8) - 1)
    return plaintext_int.to_bytes(byte_len, byteorder="little")
