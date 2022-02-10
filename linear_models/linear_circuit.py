from __future__ import annotations

from typing import List, Dict, Sequence

import numpy as np

from linear_models.linear_transformation import LinearTransformation
from models.exceptions import CircuitCycleFound
from utils.basis_vectors import get_basis_vectors
from utils.operators import xor_op


class LinearCircuit:

    def __init__(
            self,
            num_inputs: int,
            num_outputs: int,
            adjacency_matrix: np.ndarray,
    ) -> None:
        num_rows, num_columns = adjacency_matrix.shape
        assert num_rows == num_columns

        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = num_rows

        self._get_inputs_by_id = {
            node_idx: {
                input_node_idx
                for input_node_idx, is_edge in enumerate(self.adjacency_matrix[node_idx])
                if is_edge
            }
            for node_idx in range(self.num_nodes)
        }

    def _evaluate_node(
            self,
            node_idx: int,
            input_bits: Sequence[bool],
            calculation_path: List[int],
            eval_cache: Dict[int, bool],
    ) -> bool:

        if node_idx in calculation_path:
            raise CircuitCycleFound
        else:
            calculation_path = list(calculation_path)
            calculation_path.append(node_idx)

        if node_idx < self.num_inputs:
            return input_bits[node_idx]

        if node_idx in eval_cache:
            return eval_cache[node_idx]

        res = xor_op(
            self._evaluate_node(input_node_idx, input_bits, calculation_path, eval_cache)
            for input_node_idx in self._get_inputs_by_id[node_idx]
        )
        eval_cache[node_idx] = res
        return res

    def calc(self, input_bits: Sequence[bool]) -> List[int]:
        assert len(input_bits) == self.num_inputs
        final_node = self._evaluate_node(
            node_idx=self.num_nodes - 1,
            input_bits=input_bits,
            calculation_path=[],
            eval_cache={},
        )
        return [final_node]

    def to_linear_transformation(self) -> LinearTransformation:
        return LinearTransformation(matrix=np.array(
            [
                self.calc(basis_vector)
                for basis_vector in get_basis_vectors(self.num_inputs)
            ]
        ))
