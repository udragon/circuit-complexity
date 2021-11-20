from __future__ import annotations

from typing import List, Dict, Sequence

import numpy as np

from models.circuit_model import CircuitModel
from models.exceptions import CircuitCycleFound
from models.truth_table import TruthTable
from utils.bit_utils import enumerate_bit_strings


class Circuit:

    def __init__(
            self,
            num_inputs: int,
            adjacency_matrix: np.ndarray,
            node_operators: List[int],
            model: CircuitModel,
    ) -> None:
        num_rows, num_columns = adjacency_matrix.shape
        assert num_rows == num_columns

        self.num_inputs = num_inputs
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = num_rows
        self.node_operators = node_operators
        self.model = model

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

        if self.model.with_not_leaves and node_idx < 2 * self.num_inputs:
            return not input_bits[node_idx - self.num_inputs]

        if node_idx in eval_cache:
            return eval_cache[node_idx]

        node_operator = self.model.basis[self.node_operators[node_idx]]
        res = node_operator(
            self._evaluate_node(input_node_idx, input_bits, calculation_path, eval_cache)
            for input_node_idx in self._get_inputs_by_id[node_idx]
        )
        eval_cache[node_idx] = res
        return res

    def calc(self, input_bits: Sequence[bool]) -> bool:
        assert len(input_bits) == self.num_inputs
        return self._evaluate_node(
            node_idx=self.num_nodes - 1,
            input_bits=input_bits,
            calculation_path=[],
            eval_cache={},
        )

    def to_truth_table(self) -> TruthTable:
        bit_string = [
            self.calc(input_bits)
            for input_bits in enumerate_bit_strings(self.num_inputs)
        ]
        return TruthTable(bit_string=bit_string)
