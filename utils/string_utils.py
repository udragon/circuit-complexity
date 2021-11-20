from typing import Set, Iterator, TypeVar, Tuple

AlphabetType = TypeVar("AlphabetType")


def enumerate_strings(size: int, alphabet: Set[AlphabetType]) -> Iterator[Tuple[AlphabetType, ...]]:
    if size == 0:
        yield tuple()
    else:
        for string in enumerate_strings(size=size - 1, alphabet=alphabet):
            for character in alphabet:
                yield string + (character, )
