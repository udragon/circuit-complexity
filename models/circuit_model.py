from dataclasses import dataclass
from typing import Sequence, Callable, Iterable

from utils.operators import nand_op, and_op, or_op, xor_op, identity_op, nor_op

Operator = Callable[[Iterable[bool]], bool]


@dataclass
class CircuitModel:
    basis: Sequence[Operator] = (nand_op, )
    fan_in: int = 2
    with_not_leaves: bool = False


NAND_CIRCUIT_MODEL = CircuitModel(
    basis=(nand_op, ),
    fan_in=2,
    with_not_leaves=False,
)


STANDARD_CIRCUIT_MODEL = CircuitModel(
    basis=(and_op, or_op),
    fan_in=2,
    with_not_leaves=True,
)


WIDE_BASIS_CIRCUIT_MODEL = CircuitModel(
    basis=(and_op, or_op, nand_op, nor_op, xor_op),
    fan_in=2,
    with_not_leaves=True,
)
