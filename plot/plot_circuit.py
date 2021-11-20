from typing import List, Optional

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def calculate_layer_dict(edges: np.array):
    num_nodes, num_columns = edges.shape
    assert num_nodes == num_columns

    res = {}
    marked_nodes = set()
    layer = 0
    while len(marked_nodes) != num_nodes:
        layer_nodes = set()
        for node, row in enumerate(edges):
            if node not in marked_nodes:
                if all(input_node in marked_nodes for input_node, is_input in enumerate(row) if is_input):
                    res[node] = layer
                    layer_nodes.add(node)
        marked_nodes.update(layer_nodes)
        if not layer_nodes:
            return res
        layer += 1
    return res


def plot_circuit(edges: np.array, axis: Optional[plt.axis] = None, show=True) -> None:
    graph = nx.DiGraph(edges.T)
    nx.set_node_attributes(graph, values=calculate_layer_dict(edges), name="subset")
    nx.draw(graph, pos=nx.multipartite_layout(graph), ax=axis)
    if show:
        plt.show()


def plot_multiple_circuits(edges_list: List[np.array]) -> None:
    num_plots = len(edges_list)
    assert num_plots <= 8
    fig, axis_list = plt.subplots(1, num_plots, figsize=(num_plots * 2, 2))
    for edges, axis in zip(edges_list, axis_list):
        plot_circuit(edges, axis=axis, show=False)
    plt.show()
