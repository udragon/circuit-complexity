from __future__ import annotations

from typing import List

import numpy as np


class LinearTransformation:
    def __init__(self, matrix: np.ndarray) -> None:
        self.matrix = matrix
        self.rows, self.columns = matrix.shape

    @property
    def variables(self) -> int:
        return self.rows

    def calc(self, input_bits: List[bool]) -> List[bool]:
        return list(self.matrix * np.array(input_bits))

    def __repr__(self):
        return f"LT(matrix={self.matrix})"

    def __hash__(self) -> int:
        return hash(self.matrix.tostring())

    def __eq__(self, other) -> bool:
        return np.all(np.equal(self.matrix, other.matrix))
