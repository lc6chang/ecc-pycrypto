import os
import typing

from ecc import curve
from ecc import utils
from ecc import math_utils


def elgamal_encrypt(
    plaintext: curve.Point,
    public_key: curve.Point,
    rand_func: typing.Callable[[int], bytes] | None = None,
) -> tuple[curve.Point, curve.Point]:
    rand_func = rand_func or os.urandom
    curve_ = public_key.curve

    G = curve_.G  # Base point G
    M = plaintext
    k = utils.random_int_exclusive(curve_.n, rand_func)

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


def ecdh_shared(
    self_private_key: int,
    other_public_key: curve.Point,
) -> curve.Point:
    return self_private_key * other_public_key


def ecdsa_sign(
    message: bytes,
    private_key: int,
    curve_: curve.Curve,
    hash_func: typing.Callable[[bytes], int] | None = None,
    rand_func: typing.Callable[[int], bytes] | None = None,
) -> tuple[int, int]:
    hash_func = hash_func or utils.sha256
    rand_func = rand_func or os.urandom

    e = hash_func(message)
    n = curve_.n
    z = e & (2**n.bit_length() - 1)
    while True:
        k = utils.random_int_exclusive(n, rand_func)
        x = (k * curve_.G).x
        r = x % n
        if r == 0:
            continue
        s = (math_utils.modinv(k, n) * (z + r * private_key)) % n
        if s == 0:
            continue
        break
    return r, s


def ecdsa_verify(
    message: bytes,
    signature: tuple[int, int],
    public_key: curve.Point,
    hash_func: typing.Callable[[bytes], int] | None = None,
) -> bool:
    hash_func = hash_func or utils.sha256
    curve_ = public_key.curve
    n = curve_.n
    r, s = signature

    if public_key == curve_.O:
        return False
    if r < 1 or r > n - 1:
        return False
    if s < 1 or s > n - 1:
        return False

    e = hash_func(message)
    z = e & (2**n.bit_length() - 1)
    u1 = (z * math_utils.modinv(s, n)) % n
    u2 = (r * math_utils.modinv(s, n)) % n
    p = u1 * curve_.G + u2 * public_key
    if p == curve_.O:
        return False
    return r == p.x % n
