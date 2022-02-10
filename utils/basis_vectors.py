from typing import List

import numpy as np


def e_i(index: int, size: int) -> np.ndarray:
    res = np.zeros(size, dtype=np.bool)
    res[index] = True
    return res


def get_basis_vectors(size: int) -> List[np.ndarray]:
    return [e_i(index, size) for index in range(size)]
