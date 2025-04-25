import os
import typing

from ecc import curve
from ecc import utils


def gen_key_pair(
    curve_: curve.Curve,
    rand_func: typing.Callable[[int], bytes] | None = None,
) -> tuple[int, curve.Point]:
    rand_func = rand_func or os.urandom
    private_key = gen_private_key(curve_, rand_func)
    public_key = get_public_key(private_key, curve_)
    return private_key, public_key


def gen_private_key(
    curve_: curve.Curve,
    rand_func: typing.Callable[[int], bytes] | None = None,
) -> int:
    rand_func = rand_func or os.urandom
    order = curve_.n
    return utils.random_int_exclusive(order, rand_func)


def get_public_key(d: int, curve_: curve.Curve) -> curve.Point:
    assert 1 <= d < curve_.n
    return d * curve_.G
