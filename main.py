import logging

from hardness import compute_hardness_dict
from models.circuit_model import STANDARD_CIRCUIT_MODEL
from plot.plot_hardness import plot_hardness_dict


def main():
    logging.basicConfig(level=logging.INFO)
    hardness_dict = compute_hardness_dict(
        circuit_model=STANDARD_CIRCUIT_MODEL,
        num_inputs=2,
    )
    plot_hardness_dict(hardness_dict, circuit_type='Standard', num_inputs=2)


if __name__ == '__main__':
    main()
