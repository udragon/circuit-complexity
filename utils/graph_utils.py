from typing import List, Iterator, Tuple

import numpy as np

from utils.bit_utils import enumerate_bit_strings, bits_to_index


def enumerate_simple_acyclic_digraphs_adjacency_matrices(
        size: int,
        sources: int,
        sinks: int = 1,
        fan_in: int = 2,
) -> Iterator[np.ndarray]:
    """
        - Must not contains self-loops and cycles
        - Identical nodes shouldn't exists
        - must have at least 1 output per node that is not a source or a sink.
        - must have at least 2 and at most fan_in inputs per node that is not a source.
    """
    assert sources + sinks <= size
    current_rows = [(False, ) * size] * sources
    for rows in recursive_row_generator(current_rows=current_rows, sources=sources, sinks=sinks, fan_in=fan_in):
        yield np.array(rows, dtype=np.bool)


def recursive_row_generator(
        current_rows: List[Tuple[bool, ...]],
        sources: int,
        sinks: int = 1,
        fan_in: int = 2,
) -> Iterator[List[bool]]:
    node_index = len(current_rows)
    size = len(current_rows[0])
    if size == node_index:
        yield current_rows
    else:
        for row in add_new_row(current_rows=current_rows, sources=sources, sinks=sinks, fan_in=fan_in):
            yield from recursive_row_generator(
                current_rows=current_rows + [row],
                sources=sources,
                sinks=sinks,
                fan_in=fan_in
            )


def add_new_row(
        current_rows: List[Tuple[bool, ...]],
        sources: int,
        sinks: int = 1,
        fan_in: int = 2,
) -> Iterator[Tuple[bool, ...]]:
    node_index = len(current_rows)
    size = len(current_rows[0])
    remaining_nodes = size - node_index

    nodes_with_outputs = [any(row[i] for row in current_rows) for i in range(sources, node_index + 1)]
    last_row_idx = bits_to_index(reversed(current_rows[-1]))

    # Inputs can only be previous nodes.
    for row_base in enumerate_bit_strings(node_index, min_ones=2, max_ones=fan_in):

        row: Tuple[bool, ...] = (
                row_base
                + (False, ) * remaining_nodes
        )

        # Node identity does not matter.
        new_row_idx = bits_to_index(reversed(row))
        if new_row_idx <= last_row_idx:
            continue

        # All nodes must have output (except sinks & sources).
        nodes_with_no_output_yet = sum(
            (not has_output) and (not is_input_of_new_node)
            for has_output, is_input_of_new_node in zip(nodes_with_outputs, row[sources: node_index + 1])
        )
        if nodes_with_no_output_yet - sinks > (remaining_nodes - 1) * (fan_in - 1):
            continue

        yield row
