import random
import os
import typing

from ecc import curve


def elgamal_encrypt(
    plaintext: curve.Point,
    public_key: curve.Point,
    rand_func: typing.Callable[[int], bytes] | None = None,
) -> tuple[curve.Point, curve.Point]:
    rand_func = rand_func or os.urandom
    curve_ = public_key.curve

    G = curve_.G  # Base point G
    M = plaintext
    random.seed(rand_func(1024))
    k = random.randint(1, curve_.n)

    C1 = k * G
    C2 = M + k * public_key
    return C1, C2


def elgamal_decrypt(
    private_key: int,
    C1: curve.Point,
    C2: curve.Point,
) -> curve.Point:
    M = C2 + (C1.curve.n - private_key) * C1
    return M
