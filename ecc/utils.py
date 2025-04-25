import typing


def byte_length(n: int) -> int:
    assert n >= 0
    return (n.bit_length() + 7) // 8


def random_nbits_int(
    num_bits: int,
    rand_func: typing.Callable[[int], bytes],
) -> int:
    assert num_bits >= 0
    num_bytes = (num_bits + 7) // 8
    random_bytes = rand_func(num_bytes)
    random_int = int.from_bytes(random_bytes, byteorder='big')
    mask = (1 << num_bits) - 1
    return random_int & mask
