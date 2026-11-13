from itertools import combinations

def variable_id(row: int, col: int, value: int, n: int) -> int:
    """Return the SAT variable ID for a cell and its value."""
    return (row * n + col) * n + value

def encode_cells(n: int) -> list[list[int]]:
    """Encode exactly one value per cell using pairwise constraints."""
    clauses = []

    for row in range(n):
        for col in range(n):
            variables = [
                variable_id(row, col, value, n)
                for value in range(1, n + 1)
            ]

            # At least one value must be assigned
            clauses.append(variables)

            # No two values can be assigned at the same time
            for a, b in combinations(variables, 2):
                clauses.append([-a, -b])

    return clauses