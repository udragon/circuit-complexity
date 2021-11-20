from typing import Iterator, Optional, Tuple, List, Iterable


def enumerate_bit_strings(size: int, min_ones: int = 0, max_ones: Optional[int] = None) -> Iterator[Tuple[bool, ...]]:
    if size == 0:
        yield tuple()
    elif min_ones == size:
        yield (True, ) * size
    else:
        for string in enumerate_bit_strings(size - 1, min_ones=(min_ones - 1), max_ones=max_ones):
            ones_count = sum(string)
            if ones_count > min_ones - 1:
                yield string + (False, )
            if max_ones is None or ones_count < max_ones:
                yield string + (True, )


def bits_to_index(bits: Iterable[bool]) -> int:
    res = 0
    for bit in bits:
        res *= 2
        res += bit
    return res


def bit_string_to_repr_string(bit_string: List[bool]) -> str:
    return ''.join([str(int(bit)) for bit in bit_string])
