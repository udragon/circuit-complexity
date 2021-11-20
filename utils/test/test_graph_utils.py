import unittest

import numpy as np
import numpy.testing

from utils.graph_utils import enumerate_simple_acyclic_digraphs_adjacency_matrices


class GraphUtilsTest(unittest.TestCase):
    def test_enumerate_simple_acyclic_digraphs_matrices_size_3_source_2(self) -> None:
        enumerator = enumerate_simple_acyclic_digraphs_adjacency_matrices(
            size=3,
            sources=2,
            sinks=1,
            fan_in=2,
        )
        result = list(enumerator)
        expected_result = [
            np.array([
                [False, False, False],
                [False, False, False],
                [True, True, False],
            ], dtype=np.bool)
        ]
        self.assertEqual(len(result), len(expected_result))
        for matrix, expected_matrix in zip(result, expected_result):
            numpy.testing.assert_array_equal(matrix, expected_matrix)

    def test_enumerate_simple_acyclic_digraphs_matrices_size_4_source_2(self) -> None:
        enumerator = enumerate_simple_acyclic_digraphs_adjacency_matrices(
            size=4,
            sources=2,
            sinks=1,
            fan_in=2,
        )
        result = list(enumerator)
        matrix_1 = np.array([
            [False, False, False, False],
            [False, False, False, False],
            [True, True, False, False],
            [False, True, True, False],
        ], dtype=bool)
        matrix_2 = np.array([
            [False, False, False, False],
            [False, False, False, False],
            [True, True, False, False],
            [True, False, True, False],
        ], dtype=bool)
        expected_result = [matrix_1, matrix_2]
        self.assertEqual(len(result), len(expected_result))
        for matrix, expected_matrix in zip(result, expected_result):
            numpy.testing.assert_array_equal(matrix, expected_matrix)

    def test_enumerate_simple_acyclic_digraphs_matrices_size_4_source_3(self) -> None:
        enumerator = enumerate_simple_acyclic_digraphs_adjacency_matrices(
            size=4,
            sources=3,
            sinks=1,
            fan_in=2,
        )
        result = list(enumerator)
        print(result)
        expected_result = [
            np.array([
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [False,  True,  True, False]
            ]),
            np.array([
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [True, False,  True, False]
            ]),
            np.array([
                [False, False, False, False],
                [False, False, False, False],
                [False, False, False, False],
                [True,  True, False, False]
            ])
        ]
        self.assertEqual(len(result), len(expected_result))
        for matrix, expected_matrix in zip(result, expected_result):
            numpy.testing.assert_array_equal(matrix, expected_matrix)
