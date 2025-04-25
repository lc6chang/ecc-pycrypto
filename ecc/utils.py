def byte_length(n: int) -> int:
    assert n >= 0
    return (n.bit_length() + 7) // 8
