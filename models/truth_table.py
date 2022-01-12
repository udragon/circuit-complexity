from __future__ import annotations

from itertools import permutations
from math import log2
from typing import List, Set, Tuple, FrozenSet

from utils.bit_utils import bits_to_index, bit_string_to_repr_string, permute_list, index_to_bits
from utils.collection_utils import powerset


class TruthTable:
    def __init__(self, bit_string: List[bool]) -> None:
        self.bit_string = bit_string

    @classmethod
    def from_repr(cls, repr_string: str) -> TruthTable:
        return cls(
            bit_string=[bool(int(bit_str)) for bit_str in repr_string[3:-1]]
        )

    @property
    def variables(self) -> int:
        return int(log2(len(self.bit_string)))

    def calc(self, input_bits: List[bool]) -> bool:
        return self.bit_string[bits_to_index(input_bits)]

    def __repr__(self):
        return f"TT({bit_string_to_repr_string(self.bit_string)})"

    def __hash__(self) -> int:
        return bits_to_index(self.bit_string)

    def __eq__(self, other) -> bool:
        return self.bit_string == other.bit_string

    def sort_key(self):
        return sum(self.bit_string), tuple(self.bit_string)

    def permute_all(self) -> Set[TruthTable]:
        variables = self.variables
        return {
            self.permute(permutation)
            for permutation in permutations(range(variables))
        }

    def permute(self, perm: Tuple[int, ...]) -> TruthTable:
        variables = self.variables
        new_bit_string = [False] * len(self.bit_string)
        for index, bit in enumerate(self.bit_string):
            new_index = bits_to_index(permute_list(index_to_bits(index, size=variables), perm))
            new_bit_string[new_index] = bit
        return TruthTable(bit_string=new_bit_string)

    def negate_output(self) -> TruthTable:
        return TruthTable(bit_string=[not bit for bit in self.bit_string])

    def negate_variables_all(self) -> Set[TruthTable]:
        return {
            self.negate_variables(variable_indices)
            for variable_indices in powerset(range(self.variables))
        }

    def negate_variables(self, variable_indices: Set[int]) -> TruthTable:
        if not variable_indices:
            return self
        variables = self.variables
        new_bit_string = [False] * len(self.bit_string)
        for index, bit in enumerate(self.bit_string):
            index_in_bits = index_to_bits(index, size=variables)
            for variable_index in variable_indices:
                index_in_bits[variable_index] = not index_in_bits[variable_index]
            new_index = bits_to_index(index_in_bits)
            new_bit_string[new_index] = bit
        return TruthTable(bit_string=new_bit_string)

    def get_equivalent_group(self) -> FrozenSet[TruthTable]:
        all_permutations = self.permute_all()
        all_permutations_and_variable_negations = {
            tt
            for permutation in all_permutations
            for tt in permutation.negate_variables_all()
        }
        negated_outputs = {truth_table.negate_output() for truth_table in all_permutations_and_variable_negations}
        return frozenset(all_permutations_and_variable_negations | negated_outputs)
