import logging
from pprint import pprint

from hardness import (
    serialize_hardness_dict,
    equivalence_analysis,
    deserialize_hardness_dict, compute_linear_transformations_hardness_dict,
    equivalence_analysis_for_linear_transformations,
)
from linear_models.linear_transformation import LinearTransformation
from linear_models.linear_transformation_class import LinearTransformationClass
from models.circuit_model import (
    ALL_BASIS_CIRCUIT_MODEL,
)
from plot.plot_hardness import plot_hardness_dict


def main_linear():
    logging.basicConfig(level=logging.INFO)
    hardness_dict = compute_linear_transformations_hardness_dict(
        num_inputs=3,
        num_outputs=2,
        size_limit=None,
    )
    max_hardness = max(hardness_dict.values())
    lt_of_max_hardness = {
        lt
        for lt, hardness in hardness_dict.items()
        if hardness == max_hardness
    }
    print(f"Found {len(lt_of_max_hardness)} linear transformations of max hardness.")
    lt_classes = equivalence_analysis_for_linear_transformations(lt_of_max_hardness)
    print(f"Found {len(lt_classes)} linear transformations classes of max hardness.")
    pprint([LinearTransformationClass.from_lt_collection(lt_class) for lt_class in lt_classes])


def main():
    logging.basicConfig(level=logging.INFO)
    """
    hardness_dict = compute_hardness_dict(
        circuit_model=ALL_BASIS_CIRCUIT_MODEL,
        num_inputs=3,
        size_limit=7,
    )
    """
    hardness_dict = deserialize_hardness_dict(filename="data/n_3_full_basis_hardness.json")
    ea = equivalence_analysis(hardness_dict)
    pprint(ea)
    serialize_hardness_dict(hardness_dict)
    plot_hardness_dict(hardness_dict, circuit_type='Standard', num_inputs=3)


if __name__ == '__main__':
    main_linear()
