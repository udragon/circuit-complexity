from __future__ import annotations

from typing import Tuple


class LinearTransformation:
    def __init__(self, matrix: Tuple[Tuple[int]]) -> None:
        self.matrix = matrix
        self.hash = hash(self.matrix)

    def __repr__(self):
        return f"LT(matrix={self.matrix})"

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, other) -> bool:
        return self.hash == other.hash
