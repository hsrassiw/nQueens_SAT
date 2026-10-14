# Các encoding cho ràng buộc AMO (nhiều nhất một) và EO (đúng một)

from pysat.card import CardEnc, EncType


class VarPool:
    # tạo biến phụ mới
    def __init__(self, top):
        self.top = top

    def new(self):
        self.top += 1
        return self.top


def binomial(lits, pool):
    clauses = []
    for i in range(len(lits)):
        for j in range(i + 1, len(lits)):
            clauses.append([-lits[i], -lits[j]])
    return clauses


def binary(lits, pool):
    n = len(lits)
    k = 0
    while 2 ** k < n:
        k += 1
    ys = []
    for j in range(k):
        ys.append(pool.new())
    clauses = []
    for i in range(n):
        for j in range(k):
            bit = (i // 2 ** j) % 2
            if bit == 1:
                clauses.append([-lits[i], ys[j]])
            else:
                clauses.append([-lits[i], -ys[j]])
    return clauses


def pysat_amo(lits, pool, enc_type):
    cnf = CardEnc.atmost(lits=lits, bound=1, top_id=pool.top, encoding=enc_type)
    if cnf.nv > pool.top:
        pool.top = cnf.nv
    return cnf.clauses


def binary_pysat(lits, pool):
    return pysat_amo(lits, pool, EncType.bitwise)


ENCODINGS = {
    "binomial": binomial,
    "binary": binary,
    "binary_pysat": binary_pysat,
}


def at_most_one(lits, encoding, pool):
    return ENCODINGS[encoding](lits, pool)


def exactly_one(lits, encoding, pool):
    return [lits] + at_most_one(lits, encoding, pool)
