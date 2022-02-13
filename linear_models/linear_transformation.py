from __future__ import annotations

import itertools
from typing import Tuple, Set, Sequence


class LinearTransformation:
    def __init__(self, matrix: Sequence[Sequence[int]]) -> None:
        self.matrix = matrix
        self.num_rows = len(self.matrix)
        self.num_columns = len(self.matrix[0])
        self.hash = hash(self.matrix)

    def __repr__(self):
        return f"LT(matrix={self.matrix})"

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, other) -> bool:
        return self.hash == other.hash

    def sort_key(self):
        return self.matrix

    def create_linear_transformation_class(self) -> Set[LinearTransformation]:
        linear_transformation_class: Set[LinearTransformation] = set()
        for row_permutation in itertools.permutations(range(self.num_rows)):
            for column_permutation in itertools.permutations(range(self.num_columns)):
                new_matrix = tuple(
                    tuple(self.matrix[j][i] for i in column_permutation)
                    for j in row_permutation
                )
                linear_transformation_class.add(LinearTransformation(matrix=new_matrix))
        return linear_transformation_class
