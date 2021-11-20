import logging
from typing import Set, Dict, Optional

from circuit_enumeration import enumerate_circuits
from models.circuit_model import CircuitModel
from models.exceptions import CircuitCycleFound
from models.truth_table import TruthTable


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
    logging.info(f"Enumerated on {counter} circuits.")
    return truth_tables


def compute_hardness_dict(
        circuit_model: CircuitModel,
        num_inputs: int,
        size_limit: Optional[int] = None,
) -> Dict[TruthTable, int]:
    num_truth_tables = 2**(2**num_inputs)

    circuit_size = 1
    tt_collection = compute_truth_tables(
        circuit_model=circuit_model,
        num_inputs=num_inputs,
        circuit_size=circuit_size,
    )
    res = {tt: circuit_size for tt in tt_collection}
    while len(res) != num_truth_tables and (size_limit is None or circuit_size + 1 <= size_limit):
        logging.info(f"Found {len(res)} /  {num_truth_tables} truth tables.")
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
    return res
