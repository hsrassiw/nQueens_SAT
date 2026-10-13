"""Independent solution checker.

A solution is a list ``queens`` of length N where ``queens[r]`` is the column
of the queen in row r. It is valid when no two queens share a column, a
diagonal (r - c) or an anti-diagonal (r + c). Rows are distinct by construction.
"""


def is_valid(n, queens):
    if queens is None or len(queens) != n:
        return False
    if any(not 0 <= c < n for c in queens):
        return False
    columns = set(queens)
    diagonals = {r - c for r, c in enumerate(queens)}
    anti_diagonals = {r + c for r, c in enumerate(queens)}
    return len(columns) == len(diagonals) == len(anti_diagonals) == n
