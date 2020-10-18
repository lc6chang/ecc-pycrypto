from os import urandom
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ecc.math_utils.mod_inverse import modinv
from ecc.math_utils.mod_sqrt import modsqrt
from ecc.utils import int_length_in_byte


@dataclass
class Point:
    x: Optional[int]
    y: Optional[int]
    curve: "Curve"

    def is_at_infinity(self) -> bool:
        return self.x is None and self.y is None

    def __post_init__(self):
        if not self.is_at_infinity() and not self.curve.is_on_curve(self):
            raise ValueError("The point is not on the curve.")

    def __str__(self):
        if self.is_at_infinity():
            return f"Point(At infinity, Curve={str(self.curve)})"
        else:
            return f"Point(X={self.x}, Y={self.y}, Curve={str(self.curve)})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __neg__(self):
        return self.curve.neg_point(self)

    def __add__(self, other):
        return self.curve.add_point(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        negative = - other
        return self.__add__(negative)

    def __mul__(self, scalar: int):
        return self.curve.mul_point(scalar, self)

    def __rmul__(self, scalar: int):
        return self.__mul__(scalar)


@dataclass
class Curve(ABC):
    name: str
    a: int
    b: int
    p: int
    n: int
    G_x: int
    G_y: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.a == other.a and self.b == other.b and self.p == other.p and
            self.n == other.n and self.G_x == other.G_x and self.G_y == other.G_y
        )

    @property
    def G(self) -> Point:
        return Point(self.G_x, self.G_y, self)

    @property
    def INF(self) -> Point:
        return Point(None, None, self)

    def is_on_curve(self, P: Point) -> bool:
        if P.curve != self:
            return False
        return P.is_at_infinity() or self._is_on_curve(P)

    @abstractmethod
    def _is_on_curve(self, P: Point) -> bool:
        pass

    def add_point(self, P: Point, Q: Point) -> Point:
        if (not self.is_on_curve(P)) or (not self.is_on_curve(Q)):
            raise ValueError("The points are not on the curve.")
        if P.is_at_infinity():
            return Q
        elif Q.is_at_infinity():
            return P

        if P == Q:
            return self._double_point(P)
        return self._add_point(P, Q)

    @abstractmethod
    def _add_point(self, P: Point, Q: Point) -> Point:
        pass

    def double_point(self, P: Point) -> Point:
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return P

        return self._double_point(P)

    @abstractmethod
    def _double_point(self, P: Point) -> Point:
        pass

    def mul_point(self, d: int, P: Point) -> Point:
        """
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return P

        res = None
        is_negative_scalar = d < 0
        d = -d if is_negative_scalar else d
        tmp = P
        while d:
            if d & 0x1 == 1:
                if res:
                    res = self.add_point(res, tmp)
                else:
                    res = tmp
            tmp = self.double_point(tmp)
            d >>= 1
        if is_negative_scalar:
            return -res
        else:
            return res

    def neg_point(self, P: Point) -> Point:
        if not self.is_on_curve(P):
            raise ValueError("The point is not on the curve.")
        if P.is_at_infinity():
            return P

        return Point(P.x, -P.y % self.p, self)

    @abstractmethod
    def compute_y(self, x: int) -> int:
        pass

    def encode_point(self, plaintext: bytes) -> Point:
        plaintext = len(plaintext).to_bytes(1, byteorder="big") + plaintext
        while True:
            x = int.from_bytes(plaintext, "big")
            y = self.compute_y(x)
            if y:
                return Point(x, y, self)
            plaintext += urandom(1)

    def decode_point(self, M: Point) -> bytes:
        byte_len = int_length_in_byte(M.x)
        plaintext_len = (M.x >> ((byte_len - 1) * 8)) & 0xff
        plaintext = ((M.x >> ((byte_len - plaintext_len - 1) * 8))
                     & (int.from_bytes(b"\xff" * plaintext_len, "big")))
        return plaintext.to_bytes(plaintext_len, byteorder="big")


class ShortWeierstrassCurve(Curve):
    """
    y^2 = x^3 + a*x + b
    https://en.wikipedia.org/wiki/Elliptic_curve
    """

    def _is_on_curve(self, P: Point) -> bool:
        left = P.y * P.y
        right = (P.x * P.x * P.x) + (self.a * P.x) + self.b
        return (left - right) % self.p == 0

    def _add_point(self, P: Point, Q: Point) -> Point:
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * modinv(delta_x, self.p)
        res_x = (s * s - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return - Point(res_x, res_y, self)

    def _double_point(self, P: Point) -> Point:
        s = (3 * P.x * P.x + self.a) * modinv(2 * P.y, self.p)
        res_x = (s * s - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return - Point(res_x, res_y, self)

    def compute_y(self, x) -> int:
        right = (x * x * x + self.a * x + self.b) % self.p
        y = modsqrt(right, self.p)
        return y


class MontgomeryCurve(Curve):
    """
    by^2 = x^3 + ax^2 + x
    https://en.wikipedia.org/wiki/Montgomery_curve
    """

    def _is_on_curve(self, P: Point) -> bool:
        left = self.b * P.y * P.y
        right = (P.x * P.x * P.x) + (self.a * P.x * P.x) + P.x
        return (left - right) % self.p == 0

    def _add_point(self, P: Point, Q: Point) -> Point:
        delta_x = P.x - Q.x
        delta_y = P.y - Q.y
        s = delta_y * modinv(delta_x, self.p)
        res_x = (self.b * s * s - self.a - P.x - Q.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return - Point(res_x, res_y, self)

    def _double_point(self, P: Point) -> Point:
        up = 3 * P.x * P.x + 2 * self.a * P.x + 1
        down = 2 * self.b * P.y
        s = up * modinv(down, self.p)
        res_x = (self.b * s * s - self.a - 2 * P.x) % self.p
        res_y = (P.y + s * (res_x - P.x)) % self.p
        return - Point(res_x, res_y, self)

    def compute_y(self, x: int) -> int:
        right = (x * x * x + self.a * x * x + x) % self.p
        inv_b = modinv(self.b, self.p)
        right = (right * inv_b) % self.p
        y = modsqrt(right, self.p)
        return y


P256 = ShortWeierstrassCurve(
    name="P256",
    a=-3,
    b=41058363725152142129326129780047268409114441015993725554835256314039467401291,
    p=115792089210356248762697446949407573530086143415290314195533631308867097853951,
    n=115792089210356248762697446949407573529996955224135760342422259061068512044369,
    G_x=48439561293906451759052585252797914202762949526041747995844080717082404635286,
    G_y=36134250956749795798585127919587881956611106672985015071877198253568414405109
)

secp256k1 = ShortWeierstrassCurve(
    name="secp256k1",
    a=0x0,
    b=0x7,
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    n=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    G_x=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    G_y=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)

Curve25519 = MontgomeryCurve(
    name="Curve25519",
    a=486662,
    b=1,
    p=0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed,
    n=0x1000000000000000000000000000000014DEF9DEA2F79CD65812631A5CF5D3ED,
    G_x=0x9,
    G_y=0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9
)

M383 = MontgomeryCurve(
    name="M383",
    a=2065150,
    b=1,
    p=0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff45,
    n=0x10000000000000000000000000000000000000000000000006c79673ac36ba6e7a32576f7b1b249e46bbc225be9071d7,
    G_x=0xc,
    G_y=0x1ec7ed04aaf834af310e304b2da0f328e7c165f0e8988abd3992861290f617aa1f1b2e7d0b6e332e969991b62555e77e
)
