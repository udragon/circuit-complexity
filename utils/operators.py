from typing import Iterable


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
