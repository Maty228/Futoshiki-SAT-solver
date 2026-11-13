from itertools import combinations

def variable_id(row: int, col: int, value: int, n: int) -> int:
    """Return the SAT variable ID for a cell and its value."""
    return (row * n + col) * n + value

def exactly_one(variables: list[int]) -> list[list[int]]:
    """Encode exactly one true variable using pairwise constraints."""
    clauses = []

    clauses.append(variables)

    for a, b in combinations(variables, 2):
        clauses.append([-a, -b])

    return clauses

def encode_cells(n: int) -> list[list[int]]:
    """Each cell must contain exactly one value."""
    clauses = []

    for row in range(n):
        for col in range(n):
            variables = [
                variable_id(row, col, value, n)
                for value in range(1, n + 1)
            ]
            clauses.extend(exactly_one(variables))

    return clauses

def encode_rows(n: int) -> list[list[int]]:
    """Each value must occur exactly once in every row."""
    clauses = []

    for row in range(n):
        for value in range (1, n + 1):
            variables = [
                variable_id(row, col, value, n)
                for col in range(n)
            ]
            clauses.extend(exactly_one(variables))

    return clauses

def encode_columns(n: int) -> list[list[int]]:
    """Each value must occur exactly once in every column."""
    clauses = []

    for col in range(n):
        for value in range(1, n + 1):
            variables = [
                variable_id(row, col, value, n)
                for row in range(n)
            ]

            clauses.extend(exactly_one(variables))

    return clauses
