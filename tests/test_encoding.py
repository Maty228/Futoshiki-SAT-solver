import unittest
from operator import truediv

from futoshiki.encoding import variable_id, encode_cells, exactly_one, encode_columns, encode_rows, encode_inequalities, encode_inequality


def board_assignment(board):
    """Convert a filled board into a set of true SAT variables."""

    n = len(board)

    return {
        variable_id(row, col, board[row][col], n)
        for row in range(n)
        for col in range(n)
    }

def satisfies(clauses, true_variables):
    """Check whether an assignment satisfies all CNF clauses."""
    return all(
        any(
            literal in true_variables if literal > 0
            else -literal not in true_variables
            for literal in clause
        )
        for clause in clauses
    )


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

class TestRowColumnEncoding(unittest.TestCase):

    def test_exactly_one(self):
        self.assertEqual(exactly_one([1, 2, 3]), [
            [1, 2, 3],
            [-1, -2],
            [-1, -3],
            [-2, -3],
        ])

    def test_clause_counts(self):
        for n in (2, 3, 4, 5):

            expected = n * n * (1 + n * (n - 1) // 2)

            self.assertEqual(len(encode_cells(n)), expected)
            self.assertEqual(len(encode_rows(n)), expected)
            self.assertEqual(len(encode_columns(n)), expected)

    def test_valid_board(self):
        board = [
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2],
        ]

        clauses = (encode_cells(3) + encode_rows(3) + encode_columns(3))

        self.assertTrue(satisfies(clauses, board_assignment(board)))

    def test_duplicate_in_row(self):
        board = [
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
        ]

        assignment = board_assignment(board)

        self.assertTrue(satisfies(encode_cells(3), assignment))
        self.assertTrue(satisfies(encode_columns(3), assignment))
        self.assertFalse(satisfies(encode_rows(3), assignment))

    def test_duplicate_in_column(self):
        board = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]

        assignment = board_assignment(board)

        self.assertTrue(satisfies(encode_cells(3), assignment))
        self.assertTrue(satisfies(encode_rows(3), assignment))
        self.assertFalse(satisfies(encode_columns(3), assignment))


class TestInequalityEncoding(unittest.TestCase):

    def test_less_than_clauses(self):
        clauses = encode_inequality(3, 0, 0, "<", 0, 1)
        self.assertEqual(clauses, [
            [-1, -4],
            [-2, -4],
            [-2, -5],
            [-3, -4],
            [-3, -5],
            [-3, -6],
        ])

    def test_inequalit_clause_count(self):
        for n in (2, 3, 4, 5):
            clauses = encode_inequality(n, 0, 0, "<", 0, 1)

            self.assertEqual(len(clauses), n * (n + 1) //2)

    def test_valid_inequalities(self):
        board = [
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2],
        ]

        inequalities = [
            (0, 0, "<", 0, 1),
            (0, 2, ">", 1, 2),
            (0, 1, "<", 1, 1),
        ]

        clauses = encode_inequalities(3, inequalities)

        self.assertTrue(satisfies(clauses, board_assignment(board)))

    def test_violated_inequality(self):
        board = [
            [1, 2, 3],
            [2, 3, 1],
            [3, 1, 2],
        ]

        clauses = encode_inequality(3, 0, 0, ">", 0, 1)

        self.assertFalse(satisfies(clauses, board_assignment(board)))

    def test_equal_values(self):
        board = [
            [1, 1, 3],
            [2, 3, 1],
            [3, 2, 2],
        ]

        clauses = encode_inequality(3, 0, 0, "<", 0, 1)

        self.assertFalse(
            satisfies(clauses, board_assignment(board))
        )

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            encode_inequality(3, 0, 0, "=", 0, 1)


if __name__ == '__main__':
    unittest.main()