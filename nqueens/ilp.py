# Mô hình ILP cho N-Queens: x[r * n + c] = 1 khi ô (r, c) có quân hậu

import sys

import gurobipy as gp
from docplex.mp.model import Model
from gurobipy import GRB

from nqueens.sat_model import lines


def read_queens(n, values):
    queens = [None] * n
    for r in range(n):
        for c in range(n):
            if values[r * n + c] > 0.5:
                queens[r] = c
    return queens


def solve_cplex_mip(n):
    with Model() as model:
        x = model.binary_var_list(n * n)
        rows, cols, diags, anti_diags = lines(n)
        for line in rows + cols:
            cells = []
            for v in line:
                cells.append(x[v - 1])
            model.add_constraint(model.sum(cells) == 1)
        for line in diags + anti_diags:
            cells = []
            for v in line:
                cells.append(x[v - 1])
            model.add_constraint(model.sum(cells) <= 1)

        if model.solve() is None:
            return None
        values = []
        for v in x:
            values.append(v.solution_value)
        return read_queens(n, values)


def solve_gurobi(n):
    # tắt log của Gurobi trước khi khởi động
    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        with gp.Model(env=env) as model:
            x = []
            for i in range(n * n):
                x.append(model.addVar(vtype=GRB.BINARY))
            rows, cols, diags, anti_diags = lines(n)
            for line in rows + cols:
                cells = []
                for v in line:
                    cells.append(x[v - 1])
                model.addConstr(gp.quicksum(cells) == 1)
            for line in diags + anti_diags:
                cells = []
                for v in line:
                    cells.append(x[v - 1])
                model.addConstr(gp.quicksum(cells) <= 1)

            model.optimize()
            if model.Status != GRB.OPTIMAL:
                return None
            values = []
            for v in x:
                values.append(v.X)
            return read_queens(n, values)


SOLVERS = {
    "cplex_mip": solve_cplex_mip,
    "gurobi": solve_gurobi,
}


if __name__ == "__main__":
    n = 8
    solver = "gurobi"
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
