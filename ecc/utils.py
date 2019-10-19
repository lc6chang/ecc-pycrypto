def int_length_in_byte(n: int):
    length = 0
    while n:
        n >>= 8
        length += 1
    return length
