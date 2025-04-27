import typing
import hashlib


def random_nbits_int(
    num_bits: int,
    rand_func: typing.Callable[[int], bytes],
) -> int:
    assert num_bits > 0
    num_bytes = (num_bits + 7) // 8
    random_bytes = rand_func(num_bytes)
    random_int = int.from_bytes(random_bytes, byteorder='big')
    mask = (1 << num_bits) - 1
    return random_int & mask


def random_int_exclusive(
    stop: int,
    rand_func: typing.Callable[[int], bytes],
) -> int:
    """
    Generate random int in the range [1, stop).
    """
    assert stop > 1
    num_bits = stop.bit_length()
    rand = 0
    while rand < 1 or rand >= stop:
        rand = random_nbits_int(num_bits, rand_func)
    return rand


def sha256(m: bytes) -> int:
    return int(hashlib.sha256(m).hexdigest(), 16)
