from typing import List

from utils.bit_utils import bits_to_index, bit_string_to_repr_string


class TruthTable:
    def __init__(self, bit_string: List[bool]) -> None:
        self.bit_string = bit_string

    def calc(self, input_bits: List[bool]) -> bool:
        return self.bit_string[bits_to_index(input_bits)]

    def __repr__(self):
        return f"TT({bit_string_to_repr_string(self.bit_string)})"

    def __hash__(self) -> int:
        return bits_to_index(self.bit_string)

    def __eq__(self, other) -> bool:
        return self.bit_string == other.bit_string
