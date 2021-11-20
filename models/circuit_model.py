from dataclasses import dataclass
from typing import Sequence, Callable, Iterable

from utils.operators import nand_op, and_op, or_op

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
