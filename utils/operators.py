from typing import Iterable


def nand_op(it: Iterable[bool]) -> bool:
    return not all(it)


def and_op(it: Iterable[bool]) -> bool:
    return all(it)


def or_op(it: Iterable[bool]) -> bool:
    return any(it)
