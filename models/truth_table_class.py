from __future__ import annotations

from dataclasses import dataclass
from typing import Set, Iterable, Collection

from models.truth_table import TruthTable


@dataclass
class TruthTableClass:
    representative: TruthTable
    size: int

    @classmethod
    def from_truth_table_collection(cls, tt_set: Collection[TruthTable]) -> TruthTableClass:
        representative = min(tt_set, key=TruthTable.sort_key)
        return cls(
            representative=representative,
            size=len(tt_set)
        )
