# Mô hình SAT cho N-Queens, ô (r, c) ứng với biến r * n + c + 1

import sys

from pysat.formula import CNF
from pysat.solvers import Solver

from nqueens.amo import VarPool, at_most_one, exactly_one


def var(n, r, c):
    return r * n + c + 1


def lines(n):
    rows = [[] for _ in range(n)]
    cols = [[] for _ in range(n)]
    diags = [[] for _ in range(2 * n - 1)]
    anti_diags = [[] for _ in range(2 * n - 1)]
    for r in range(n):
        for c in range(n):
            x = var(n, r, c)
            rows[r].append(x)
            cols[c].append(x)
            diags[r - c + n - 1].append(x)
            anti_diags[r + c].append(x)
    return rows, cols, diags, anti_diags


def encode(n, encoding="binomial"):
    pool = VarPool(n * n)
    clauses = []
    rows, cols, diags, anti_diags = lines(n)
    for line in rows + cols:
        clauses += exactly_one(line, encoding, pool)
    for line in diags + anti_diags:
        if len(line) > 1:
            clauses += at_most_one(line, encoding, pool)
    return CNF(from_clauses=clauses)


def decode(n, model):
    queens = [None] * n
    for lit in model:
        if 0 < lit <= n * n:
            r = (lit - 1) // n
            c = (lit - 1) % n
            queens[r] = c
    return queens


def solve(n, encoding="binomial", solver="cadical195"):
    with Solver(name=solver, bootstrap_with=encode(n, encoding).clauses) as s:
        if not s.solve():
            return None
        return decode(n, s.get_model())


def count_solutions(n, encoding="binomial", solver="cadical195"):
    count = 0
    with Solver(name=solver, bootstrap_with=encode(n, encoding).clauses) as s:
        while s.solve():
            queens = decode(n, s.get_model())
            # chặn lời giải vừa tìm (chỉ dùng biến ô)
            block = []
            for r in range(n):
                block.append(-var(n, r, queens[r]))
            s.add_clause(block)
            count += 1
    return count


if __name__ == "__main__":
    n = 8
    encoding = "binomial"
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        encoding = sys.argv[2]
    queens = solve(n, encoding)
    if queens is None:
        print(f"N = {n}: không có lời giải")
    else:
        for r in range(n):
            row = ["."] * n
            row[queens[r]] = "Q"
            print(" ".join(row))
