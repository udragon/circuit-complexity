from __future__ import annotations

from itertools import permutations
from math import log
from typing import List, Set, Tuple, FrozenSet

from utils.bit_utils import bits_to_index, bit_string_to_repr_string, permute_list, index_to_bits


class TruthTable:
    def __init__(self, bit_string: List[bool]) -> None:
        self.bit_string = bit_string
        self.variables = int(log(log(len(bit_string))))

    def calc(self, input_bits: List[bool]) -> bool:
        return self.bit_string[bits_to_index(input_bits)]

    def __repr__(self):
        return f"TT({bit_string_to_repr_string(self.bit_string)})"

    def __hash__(self) -> int:
        return bits_to_index(self.bit_string)

    def __eq__(self, other) -> bool:
        return self.bit_string == other.bit_string

    def permute_all(self) -> Set[TruthTable]:
        return {
            self.permute(permutation)
            for permutation in permutations(range(self.variables))
        }

    def permute(self, perm: Tuple[int, ...]) -> TruthTable:
        new_bit_string = [False] * len(self.bit_string)
        for index, bit in enumerate(self.bit_string):
            new_index = bits_to_index(permute_list(index_to_bits(index), perm))
            new_bit_string[new_index] = bit
        return TruthTable(bit_string=new_bit_string)

    def negate(self) -> TruthTable:
        return TruthTable(bit_string=[not bit for bit in self.bit_string])

    def get_equivalent_group(self) -> FrozenSet[TruthTable]:
        all_permutations = self.permute_all()
        permutation_negations = {truth_table.negate() for truth_table in all_permutations}
        return frozenset(all_permutations | permutation_negations)
