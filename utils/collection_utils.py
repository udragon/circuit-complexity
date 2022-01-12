from itertools import combinations, chain
from typing import Dict, Set, TypeVar, List

KeyType = TypeVar("KeyType")
ValType = TypeVar("ValType")


def inverse_dict(d: Dict[KeyType, ValType]) -> Dict[ValType, Set[KeyType]]:
    res = {}
    for key, val in d.items():
        if val in res:
            res[val].add(key)
        else:
            res[val] = {key}
    return res


def partial_sum_list(li: List[int]) -> List[int]:
    res = []
    partial_sum = 0
    for val in li:
        partial_sum += val
        res.append(partial_sum)
    return res


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
