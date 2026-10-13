# Mô hình SAT cho bài N-Queens.
# Ô (r, c) ứng với biến r * n + c + 1, biến đúng nghĩa là ô đó có quân hậu.
# Mỗi hàng, mỗi cột có đúng một quân; mỗi đường chéo có nhiều nhất một quân.

import sys

from pysat.formula import CNF
from pysat.solvers import Solver

from nqueens.amo import VarPool, at_most_one, exactly_one


def var(n, r, c):
    return r * n + c + 1


def lines(n):
    # Trả về các hàng, cột, đường chéo chính và đường chéo phụ
    rows = [[] for _ in range(n)]
    cols = [[] for _ in range(n)]
    diags = [[] for _ in range(2 * n - 1)]       # chỉ số r - c + n - 1
    anti_diags = [[] for _ in range(2 * n - 1)]  # chỉ số r + c
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
    # Đọc lời giải: queens[r] = cột của quân hậu ở hàng r (bỏ qua biến phụ)
    queens = [None] * n
    for lit in model:
        if 0 < lit <= n * n:
            r = (lit - 1) // n
            c = (lit - 1) % n
            queens[r] = c
    return queens


def solve(n, encoding="binomial", solver="cadical195"):
    # Trả về một lời giải, hoặc None nếu không có
    with Solver(name=solver, bootstrap_with=encode(n, encoding).clauses) as s:
        if not s.solve():
            return None
        return decode(n, s.get_model())


def count_solutions(n, encoding="binomial", solver="cadical195"):
    # Đếm số lời giải: tìm được lời giải nào thì thêm mệnh đề cấm lời giải đó.
    # Mệnh đề chặn chỉ dùng biến ô, để không đếm trùng khi chỉ biến phụ khác nhau.
    count = 0
    with Solver(name=solver, bootstrap_with=encode(n, encoding).clauses) as s:
        while s.solve():
            queens = decode(n, s.get_model())
            block = []
            for r in range(n):
                block.append(-var(n, r, queens[r]))
            s.add_clause(block)
            count += 1
    return count


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    queens = solve(n)
    if queens is None:
        print(f"N = {n}: không có lời giải")
    else:
        for r in range(n):
            row = ["."] * n
            row[queens[r]] = "Q"
            print(" ".join(row))
