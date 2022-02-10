import json
import logging
from typing import Set, Dict, Optional, List

from circuit_enumeration import enumerate_circuits, enumerate_linear_circuits
from linear_models.linear_transformation import LinearTransformation
from models.circuit_model import CircuitModel
from models.exceptions import CircuitCycleFound
from models.truth_table import TruthTable
from models.truth_table_class import TruthTableClass
from utils.collection_utils import inverse_dict
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


def compute_linear_transformations(
        num_inputs: int,
        num_outputs: int,
        circuit_size: int,
) -> Set[LinearTransformation]:
    counter = 0
    linear_transformations = set()
    for linear_circuit in enumerate_linear_circuits(
            num_inputs=num_inputs,
            num_outputs=num_outputs,
            circuit_size=circuit_size
    ):
        counter += 1
        try:
            linear_transformations.add(linear_circuit.to_linear_transformation())
        except CircuitCycleFound:
            logging.error("CircuitCycleFound error")
            pass
    logging.info(f"Enumerated on {counter} linear circuits of size {circuit_size}.")
    return linear_transformations


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


@timeit
def compute_linear_transformations_hardness_dict(
        num_inputs: int,
        num_outputs: int,
        size_limit: Optional[int] = None,
) -> Dict[LinearTransformation, int]:
    num_linear_transformations = 2**(num_inputs * num_outputs)

    circuit_size = 0
    res = {}
    while len(res) != num_linear_transformations and (size_limit is None or circuit_size + 1 <= size_limit):
        circuit_size += 1
        enumerated_tts = 0
        for linear_transformation in compute_linear_transformations(
            num_inputs=num_inputs,
            num_outputs=num_outputs,
            circuit_size=circuit_size,
        ):
            enumerated_tts += 1
            if linear_transformation not in res:
                res[linear_transformation] = circuit_size
        logging.info(f"Found {len(res)} /  {num_linear_transformations} linear transformations")
    return res


def serialize_hardness_dict(hardness_dict: Dict[TruthTable, int], filename: str = "hardness.json") -> None:
    json.dump({str(tt): hardness for tt, hardness in hardness_dict.items()}, open(filename, 'w'), indent=4)


def deserialize_hardness_dict(filename: str = "hardness.json") -> Dict[TruthTable, int]:
    raw_dict = json.load(open(filename))
    return {TruthTable.from_repr(tt): hardness for tt, hardness in raw_dict.items()}


def equivalence_analysis(hardness_dict: Dict[TruthTable, int]) -> Dict[int, List[TruthTableClass]]:
    hardness_to_tt_set = inverse_dict(hardness_dict)
    return {
        hardness: equivalence_analysis_for_tts(tt_set)
        for hardness, tt_set in hardness_to_tt_set.items()
    }


def equivalence_analysis_for_tts(tt_set: Set[TruthTable]) -> List[TruthTableClass]:
    equivalent_groups = set()
    while tt_set:
        tt = tt_set.pop()
        equivalent_group = tt.get_equivalent_group()
        equivalent_groups.add(equivalent_group)
        tt_set -= equivalent_group
    return [
        TruthTableClass.from_truth_table_collection(equivalent_group)
        for equivalent_group in sorted(equivalent_groups, key=len)
    ]
