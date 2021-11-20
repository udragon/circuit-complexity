from itertools import product
from typing import Iterable, Callable, Sequence


def nand_op(it: Iterable[bool]) -> bool:
    return not all(it)


def and_op(it: Iterable[bool]) -> bool:
    return all(it)


def nor_op(it: Iterable[bool]) -> bool:
    return not any(it)


def or_op(it: Iterable[bool]) -> bool:
    return any(it)


def null_op(_: Iterable[bool]) -> bool:
    return False


def identity_op(_: Iterable[bool]) -> bool:
    return True


def xor_op(it: Iterable[bool]) -> bool:
    res = False
    for i in it:
        res ^= i
    return res


def get_all_binary_operations() -> Sequence[Callable[[Iterable[bool]], bool]]:
    res = []
    for binary_truth_table in product([False, True], repeat=4):
        res.append(lambda it, tt=binary_truth_table: tt[(next(it) * 2) + next(it)])
    return res
