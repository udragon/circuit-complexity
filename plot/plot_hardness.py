from typing import Dict

import matplotlib.pyplot as plt

from models.circuit import TruthTable
from utils.collection_utils import inverse_dict, partial_sum_list


def plot_hardness_dict(
        hardness_dict: Dict[TruthTable, int],
        circuit_type: str,
        num_inputs: int,
) -> None:

    max_hardness = max(hardness_dict.values())
    hardness_to_tt_set = inverse_dict(hardness_dict)
    tt_per_hardness = [len(hardness_to_tt_set.get(hardness, set())) for hardness in range(max_hardness + 1)]
    hardness_partial_sum = partial_sum_list(tt_per_hardness)
    num_functions = max(hardness_partial_sum)
    x_axis = list(range(max_hardness + 1))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.tight_layout(pad=5)

    ax1.plot(x_axis, hardness_partial_sum)
    ax1.set_xlim(0, max_hardness)
    ax1.set_xlabel("Hardness")
    ax1.set_ylim(0, num_functions)
    ax1.set_ylabel("# Functions")
    ax1_2 = ax1.twinx()
    ax1_2.set_ylim(0, 1)
    ax1_2.set_ylabel("Percentage")

    ax2.plot(x_axis, tt_per_hardness)
    ax2.set_xlim(0, max_hardness)
    ax2.set_xlabel("Hardness")
    ax2.set_ylim(0, max(tt_per_hardness) + 1)
    ax2.set_ylabel("# Functions")
    ax2_2 = ax2.twinx()
    ax2_2.set_ylim(0, (max(tt_per_hardness) + 1) / num_functions)
    ax2_2.set_ylabel("Percentage")

    fig.suptitle(f"Distribution of Hardness in {circuit_type} circuits with {num_inputs} inputs")
    plt.show()
