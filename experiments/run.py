# Chạy các thí nghiệm, mỗi lần giải là một tiến trình riêng, kết quả ghi vào results/<tên>.csv
# Ví dụ: python -m experiments.run e1
#        python -m experiments.run e1 16     (chỉ chạy N <= 16 để thử)

import csv
import json
import os
import resource
import signal
import subprocess
import sys

SIZES = [4, 8, 9, 16, 25, 27, 36, 49, 64, 81, 100, 125, 216, 343, 512, 729, 1000, 1331]
TIME_LIMIT = 300                  # giây
MEMORY_LIMIT = 10 * 1024 ** 3     # 10 GB, chỉ áp dụng cho SAT

ENCODINGS = ["binomial", "binary", "binary_pysat", "seqcounter", "seqcounter_pysat", "commander", "product"]
SAT_SOLVERS = ["cadical195", "glucose3", "glucose4", "kissat404", "minisat22", "lingeling", "cryptominisat"]
CP_ILP = ["cpsat", "cplex_cp", "cplex_mip", "gurobi"]
BEST_ENCODING = "product"         # chọn lại sau khi có kết quả E1

COLUMNS = ["n", "solver", "encoding", "status", "variables", "clauses",
           "encode_time", "solve_time", "total_time", "memory_mb"]


def limit_memory():
    # > MEMORY_LIMIT thì báo MemoryError
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))


def run_one(n, solver, encoding):
    cmd = [sys.executable, "-m", "experiments.run_one", str(n), solver]
    limit = None
    if encoding != "":
        cmd.append(encoding)
        limit = limit_memory

    # run_one.py thành một chương trình
    # start_new_session gom cùng các tiến trình con vào một nhóm
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            start_new_session=True, preexec_fn=limit)
    try:
        out, err = proc.communicate(timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        # quá giờ tắt cả nhóm
        os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        return {"status": "TO", "total_time": TIME_LIMIT}

    if proc.returncode != 0:
        # MemoryError hoặc OS tự tắt do hết RAM
        if "MemoryError" in err or proc.returncode == -signal.SIGKILL:
            return {"status": "MO"}
        return {"status": "ERROR"}
    return json.loads(out.strip().splitlines()[-1])


def jobs(experiment):
    result = []
    for n in SIZES:
        if experiment == "e1":
            for encoding in ENCODINGS:
                result.append((n, "cadical195", encoding))
        if experiment == "e2":
            for solver in SAT_SOLVERS:
                result.append((n, solver, BEST_ENCODING))
        if experiment == "e3":
            result.append((n, "cadical195", BEST_ENCODING))
            for solver in CP_ILP:
                result.append((n, solver, ""))
    return result


def main():
    experiment = sys.argv[1]
    max_n = SIZES[-1]
    if len(sys.argv) > 2:
        max_n = int(sys.argv[2])

    os.makedirs("results", exist_ok=True)
    path = f"results/{experiment}.csv"

    # bỏ qua những lần đã chạy, chạy tiếp được
    done = set()
    if os.path.exists(path):
        with open(path) as f:
            for row in csv.DictReader(f):
                done.add((int(row["n"]), row["solver"], row["encoding"]))
    else:
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(COLUMNS)

    for n, solver, encoding in jobs(experiment):
        if n > max_n or (n, solver, encoding) in done:
            continue
        row = run_one(n, solver, encoding)
        row["n"] = n
        row["solver"] = solver
        row["encoding"] = encoding
        print(n, solver, encoding, row["status"], round(row.get("total_time", 0), 2), flush=True)
        with open(path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writerow(row)


if __name__ == "__main__":
    main()
