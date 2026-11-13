import unittest
from operator import truediv

from futoshiki.encoding import variable_id, encode_cells


class TestVariableMapping(unittest.TestCase):
    def test_first_variable(self):
        self.assertEqual(variable_id(0, 0, 1, 3), 1)

    def test_last_variable(self):
        self.assertEqual(variable_id(2, 2, 3, 3), 27)

    def test_unique_variables(self):
        n = 4
        ids = {
            variable_id(row, col, value, n)
            for row in range(n)
            for col in range(n)
            for value in range (1, n+1)
        }

        self.assertEqual(len(ids), n**3)
        self.assertEqual(ids, set (range(1, n**3 + 1)))


class TestCellEncoding(unittest.TestCase):
    def test_number_of_clauses(self):
        for n in (2, 3, 4, 5):
            clauses = encode_cells(n)
            expected = n * n * (1 + n * (n - 1) // 2)
            self.assertEqual(len(clauses), expected)

    def test_first_cell(self):
        clauses = encode_cells(3)
        self.assertEqual(clauses[:4], [
            [1, 2, 3],
            [-1, -2],
            [-1, -3],
            [-2, -3]
        ])

    def test_valid_assignment(self):
        n = 3
        clauses = encode_cells(n)

        # Assign the value 1 to every cell
        true_variables = {
            variable_id(row, col, 1, n)
            for row in range(n)
            for col in range(n)
        }

        for clause in clauses:
            self.assertTrue(any(
                (literal > 0) == (abs(literal) in true_variables)
               for literal in clause
            ))

    def test_invalid_assignment(self):
        clauses = encode_cells(3)


        # First cell has both values 1 and 2
        true_variables = {1, 2}
        self.assertFalse(any(
            (literal > 0) == (abs(literal) in true_variables)
            for literal in [-1, -2]
        ))

if __name__ == '__main__':
    unittest.main()