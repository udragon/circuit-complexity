from __future__ import annotations

from dataclasses import dataclass
from typing import Collection

from linear_models.linear_transformation import LinearTransformation


@dataclass
class LinearTransformationClass:
    representative: LinearTransformation
    size: int

    @classmethod
    def from_lt_collection(cls, tt_set: Collection[LinearTransformation]) -> LinearTransformationClass:
        representative = min(tt_set, key=LinearTransformation.sort_key)
        return cls(
            representative=representative,
            size=len(tt_set)
        )
