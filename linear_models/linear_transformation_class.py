from __future__ import annotations

from dataclasses import dataclass
from typing import Collection, Tuple

from linear_models.linear_transformation import LinearTransformation


@dataclass
class LinearTransformationClass:
    representative: LinearTransformation
    size: int
    sparsity: int

    @classmethod
    def from_lt_collection(cls, tt_set: Collection[LinearTransformation]) -> LinearTransformationClass:
        representative = min(tt_set, key=LinearTransformation.sort_key)
        return cls(
            representative=representative,
            size=len(tt_set),
            sparsity=representative.sparsity,
        )

    def sort_key(self) -> Tuple[int, int]:
        return self.sparsity, -self.size
