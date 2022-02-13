from __future__ import annotations

from dataclasses import dataclass
from typing import Collection

from models.truth_table import TruthTable


@dataclass
class TruthTableClass:
    representative: TruthTable
    size: int

    @classmethod
    def from_truth_table_collection(cls, lt_set: Collection[TruthTable]) -> TruthTableClass:
        representative = min(lt_set, key=TruthTable.sort_key)
        return cls(
            representative=representative,
            size=len(lt_set)
        )
