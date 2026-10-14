# Mô hình CP cho N-Queens: q[r] là cột của quân hậu ở hàng r

import os
import sys

from docplex.cp.model import CpoModel
from ortools.sat.python import cp_model

CPOPTIMIZER = os.path.expanduser("~/ibm/CPLEX_Studio2220/cpoptimizer/bin/x86-64_linux/cpoptimizer")


def solve_cpsat(n):
    model = cp_model.CpModel()
    q = []
    for r in range(n):
        q.append(model.new_int_var(0, n - 1, f"q{r}"))
    diag1 = []
    diag2 = []
    for r in range(n):
        diag1.append(q[r] + r)
        diag2.append(q[r] - r)
    model.add_all_different(q)
    model.add_all_different(diag1)
    model.add_all_different(diag2)

    solver = cp_model.CpSolver()
    status = solver.solve(model)
    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        return None
    queens = []
    for r in range(n):
        queens.append(solver.value(q[r]))
    return queens


def solve_cplex_cp(n):
    model = CpoModel()
    q = []
    for r in range(n):
        q.append(model.integer_var(0, n - 1, f"q{r}"))
    diag1 = []
    diag2 = []
    for r in range(n):
        diag1.append(q[r] + r)
        diag2.append(q[r] - r)
    model.add(model.all_diff(q))
    model.add(model.all_diff(diag1))
    model.add(model.all_diff(diag2))

    result = model.solve(execfile=CPOPTIMIZER, LogVerbosity="Quiet")
    if not result:
        return None
    queens = []
    for r in range(n):
        queens.append(result[q[r]])
    return queens


SOLVERS = {
    "cpsat": solve_cpsat,
    "cplex_cp": solve_cplex_cp,
}


if __name__ == "__main__":
    n = 8
    solver = "cpsat"
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        solver = sys.argv[2]
    queens = SOLVERS[solver](n)
    if queens is None:
        print(f"N = {n}: không có lời giải")
    else:
        for r in range(n):
            row = ["."] * n
            row[queens[r]] = "Q"
            print(" ".join(row))
