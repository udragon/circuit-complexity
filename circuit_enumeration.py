from typing import Iterator

from linear_models.linear_circuit import LinearCircuit
from models.circuit import Circuit
from models.circuit_model import CircuitModel
from utils.graph_utils import enumerate_simple_acyclic_digraphs_adjacency_matrices
from utils.string_utils import enumerate_strings


def enumerate_circuits(
        circuit_model: CircuitModel,
        num_inputs: int,
        circuit_size: int,
) -> Iterator[Circuit]:
    num_sources = (
        num_inputs
        if not circuit_model.with_not_leaves
        else num_inputs * 2
    )
    if circuit_size < num_sources + 1:
        return

    for adjacency_matrix in enumerate_simple_acyclic_digraphs_adjacency_matrices(
            size=circuit_size,
            sources=num_sources,
            sinks=1,
            fan_in=circuit_model.fan_in,
    ):
        for bit_string in enumerate_strings(
                alphabet=set(range(len(circuit_model.basis))),
                size=circuit_size - num_sources,
        ):
            yield Circuit(
                num_inputs=num_inputs,
                adjacency_matrix=adjacency_matrix,
                node_operators=([0] * num_sources) + [int(bit) for bit in bit_string],
                model=circuit_model,
            )


def enumerate_linear_circuits(
        num_inputs: int,
        num_outputs: int,
        circuit_size: int,
) -> Iterator[LinearCircuit]:
    if circuit_size < num_inputs + 1:
        return

    for adjacency_matrix in enumerate_simple_acyclic_digraphs_adjacency_matrices(
            size=circuit_size,
            sources=num_inputs,
            sinks=num_outputs,
            fan_in=2,
    ):
        yield LinearCircuit(
            num_inputs=num_inputs,
            output_nodes=[circuit_size - 1],
            adjacency_matrix=adjacency_matrix,
        )
