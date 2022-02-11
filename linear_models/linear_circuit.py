from __future__ import annotations

from typing import List, Dict, Sequence, Set

import numpy as np

from linear_models.linear_transformation import LinearTransformation
from models.exceptions import CircuitCycleFound
from utils.basis_vectors import get_basis_vectors
from utils.operators import xor_op


class LinearCircuit:

    def __init__(
            self,
            num_inputs: int,
            possible_output_nodes: List[List[int]],
            adjacency_matrix: np.ndarray,
    ) -> None:
        num_rows, num_columns = adjacency_matrix.shape
        assert num_rows == num_columns

        self.num_inputs = num_inputs
        self.possible_output_nodes = possible_output_nodes
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
        if node_idx == -1:
            return False
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

    def calc_all(self, input_bits: Sequence[bool]) -> List[int]:
        assert len(input_bits) == self.num_inputs
        eval_cache = {}
        return [
            self._evaluate_node(
                node_idx=node_idx,
                input_bits=input_bits,
                calculation_path=[],
                eval_cache=eval_cache,
            )
            for node_idx in range(self.num_nodes)
        ]

    def to_linear_transformations(self) -> List[LinearTransformation]:
        node_values_by_basis_vector = [
            self.calc_all(input_bits=basis_vector)
            for basis_vector in get_basis_vectors(self.num_inputs)
        ]
        for node_values in node_values_by_basis_vector:
            node_values.append(False)  # to support node idx -1 => always False output
        return [
            LinearTransformation(matrix=tuple(
                    tuple(node_values[output_node] for output_node in output_nodes)
                    for node_values in node_values_by_basis_vector
                )
            )
            for output_nodes in self.possible_output_nodes
        ]

    def __repr__(self):
        return (
            f"LinearCircuit("
            f"num_inputs: {self.num_inputs}"
            f"possible_output_nodes: {self.possible_output_nodes}"
            f"adjacency_matrix: {self.adjacency_matrix}"
            f")"
        )
