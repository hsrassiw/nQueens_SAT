# Giải một lần rồi in kết quả ra một dòng JSON
# Ví dụ: python -m experiments.run_one 100 cadical195 product
#        python -m experiments.run_one 100 gurobi

import json
import resource
import sys
import time

from nqueens.sat_model import decode, encode
from nqueens.verify import is_valid

CP_ILP = ["cpsat", "cplex_cp", "cplex_mip", "gurobi"]


def solve_sat(n, solver, encoding, result):
    start = time.time()
    cnf = encode(n, encoding)
    result["variables"] = cnf.nv
    result["clauses"] = len(cnf.clauses)
    result["encode_time"] = time.time() - start

    start = time.time()
    if solver == "cryptominisat":
        import pycryptosat
        s = pycryptosat.Solver()
        s.add_clauses(cnf.clauses)
        ok, values = s.solve()
        model = []
        if ok:
            for v in range(1, n * n + 1):
                if values[v]:
                    model.append(v)
    else:
        from pysat.solvers import Solver
        with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
            ok = s.solve()
            model = s.get_model()
    result["solve_time"] = time.time() - start

    if ok:
        return decode(n, model)
    return None


def solve_cp_ilp(n, solver, result):
    # nạp thư viện trước khi tính giờ
    if solver == "cpsat" or solver == "cplex_cp":
        from nqueens.cp import SOLVERS
    else:
        from nqueens.ilp import SOLVERS
    start = time.time()
    queens = SOLVERS[solver](n)
    result["solve_time"] = time.time() - start
    return queens


def main():
    n = int(sys.argv[1])
    solver = sys.argv[2]
    encoding = ""
    if len(sys.argv) > 3:
        encoding = sys.argv[3]

    result = {"encode_time": 0}
    if solver in CP_ILP:
        queens = solve_cp_ilp(n, solver, result)
    else:
        queens = solve_sat(n, solver, encoding, result)
    result["total_time"] = result["encode_time"] + result["solve_time"]
    result["encode_time"] = round(result["encode_time"], 4)
    result["solve_time"] = round(result["solve_time"], 4)
    result["total_time"] = round(result["total_time"], 4)

    if queens is None:
        result["status"] = "UNSAT"
    elif is_valid(n, queens):
        result["status"] = "SAT"
    else:
        result["status"] = "WRONG"

    # RAM max, tính cả tiến trình con (cpoptimizer của CPLEX CP), đổi KB sang MB
    memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory += resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    result["memory_mb"] = round(memory / 1024)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
