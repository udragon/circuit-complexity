from typing import List

import numpy as np


BASIS_VECTORS = {}


def e_i(index: int, size: int) -> np.ndarray:
    res = np.zeros(size, dtype=np.bool)
    res[index] = True
    return res


def get_basis_vectors(size: int) -> List[np.ndarray]:
    if size in BASIS_VECTORS:
        return BASIS_VECTORS[size]
    basis_vectors = [e_i(index, size) for index in range(size)]
    BASIS_VECTORS[size] = basis_vectors
    return basis_vectors
