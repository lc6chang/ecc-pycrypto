import random
from os import urandom
from typing import Callable, Tuple
from dataclasses import dataclass

from ecc.curve import Curve, Point


@dataclass
class ElGamal:
    curve: Curve

    def encrypt(self, plaintext: bytes, public_key: Point,
                randfunc: Callable = None) -> Tuple[Point, Point]:
        return self.encrypt_bytes(plaintext, public_key, randfunc)

    def decrypt(self, private_key: int, C1: Point, C2: Point) -> bytes:
        return self.decrypt_bytes(private_key, C1, C2)

    def encrypt_bytes(self, plaintext: bytes, public_key: Point,
                      randfunc: Callable = None) -> Tuple[Point, Point]:
        # Encode plaintext into a curve point
        M = self.curve.encode_point(plaintext)
        return self.encrypt_point(M, public_key, randfunc)

    def decrypt_bytes(self, private_key: int, C1: Point, C2: Point) -> bytes:
        M = self.decrypt_point(private_key, C1, C2)
        return self.curve.decode_point(M)

    def encrypt_point(self, plaintext: Point, public_key: Point,
                      randfunc: Callable = None) -> Tuple[Point, Point]:
        randfunc = randfunc or urandom
        # Base point G
        G = self.curve.G
        M = plaintext

        random.seed(randfunc(1024))
        k = random.randint(1, self.curve.n)

        C1 = k * G
        C2 = M + k * public_key
        return C1, C2

    def decrypt_point(self, private_key: int, C1: Point, C2: Point) -> Point:
        M = C2 + (self.curve.n - private_key) * C1
        return M
