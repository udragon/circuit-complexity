import json
import logging
from typing import Set, Dict, Optional

from circuit_enumeration import enumerate_circuits
from models.circuit_model import CircuitModel
from models.exceptions import CircuitCycleFound
from models.truth_table import TruthTable
from utils.decorators import timeit


def compute_truth_tables(
        circuit_model: CircuitModel,
        num_inputs: int,
        circuit_size: int,
) -> Set[TruthTable]:
    counter = 0
    truth_tables = set()
    for circuit in enumerate_circuits(
            circuit_model=circuit_model,
            num_inputs=num_inputs,
            circuit_size=circuit_size
    ):
        counter += 1
        try:
            truth_tables.add(circuit.to_truth_table())
        except CircuitCycleFound:
            logging.error("CircuitCycleFound error")
            pass
    logging.info(f"Enumerated on {counter} circuits of size {circuit_size}.")
    return truth_tables


@timeit
def compute_hardness_dict(
        circuit_model: CircuitModel,
        num_inputs: int,
        size_limit: Optional[int] = None,
) -> Dict[TruthTable, int]:
    num_truth_tables = 2**(2**num_inputs)

    circuit_size = 0
    res = {}
    while len(res) != num_truth_tables and (size_limit is None or circuit_size + 1 <= size_limit):
        circuit_size += 1
        enumerated_tts = 0
        for tt in compute_truth_tables(
            circuit_model=circuit_model,
            num_inputs=num_inputs,
            circuit_size=circuit_size,
        ):
            enumerated_tts += 1
            if tt not in res:
                res[tt] = circuit_size
        logging.info(f"Found {len(res)} /  {num_truth_tables} truth tables.")
    return res


def serialize_hardness_dict(hardness_dict: Dict[TruthTable, int], filename: str = "hardness.json") -> None:
    json.dump({str(tt): hardness for tt, hardness in hardness_dict.items()}, open(filename, 'w'), indent=4)
