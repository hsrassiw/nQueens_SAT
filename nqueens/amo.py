# Các encoding cho ràng buộc AMO (nhiều nhất một) và EO (đúng một)

import math

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


def seqcounter(lits, pool):
    n = len(lits)
    if n <= 1:
        return []
    s = []
    for i in range(n - 1):
        s.append(pool.new())
    clauses = [[-lits[0], s[0]]]
    for i in range(1, n - 1):
        clauses.append([-lits[i], s[i]])
        clauses.append([-s[i - 1], s[i]])
        clauses.append([-s[i - 1], -lits[i]])
    clauses.append([-s[n - 2], -lits[n - 1]])
    return clauses


def commander(lits, pool):
    n = len(lits)
    g = math.isqrt(n)
    size = math.ceil(n / g)
    groups = []
    for start in range(0, n, size):
        groups.append(lits[start:start + size])

    clauses = []
    cs = []
    for group in groups:
        c = pool.new()
        cs.append(c)
        clauses.append([-c] + group)       # c đúng thì nhóm có quân
        clauses += binomial(group, pool)   # trong nhóm nhiều nhất một quân
        for x in group:
            clauses.append([c, -x])        # c sai thì cả nhóm không có quân
    clauses += binomial(cs, pool)          # nhiều nhất một c đúng
    return clauses


def product(lits, pool):
    n = len(lits)
    p = math.ceil(math.sqrt(n))
    q = math.ceil(n / p)
    rs = []
    for u in range(p):
        rs.append(pool.new())
    cs = []
    for v in range(q):
        cs.append(pool.new())

    clauses = binomial(rs, pool) + binomial(cs, pool)
    for i in range(n):
        u = i // q   # ô thứ i nằm ở hàng u, cột v của lưới
        v = i % q
        clauses.append([-lits[i], rs[u]])
        clauses.append([-lits[i], cs[v]])
    return clauses


def pysat_amo(lits, pool, enc_type):
    cnf = CardEnc.atmost(lits=lits, bound=1, top_id=pool.top, encoding=enc_type)
    if cnf.nv > pool.top:
        pool.top = cnf.nv
    return cnf.clauses


def binary_pysat(lits, pool):
    return pysat_amo(lits, pool, EncType.bitwise)


def seqcounter_pysat(lits, pool):
    return pysat_amo(lits, pool, EncType.seqcounter)


ENCODINGS = {
    "binomial": binomial,
    "binary": binary,
    "binary_pysat": binary_pysat,
    "seqcounter": seqcounter,
    "seqcounter_pysat": seqcounter_pysat,
    "commander": commander,
    "product": product,
}


def at_most_one(lits, encoding, pool):
    return ENCODINGS[encoding](lits, pool)


def exactly_one(lits, encoding, pool):
    return [lits] + at_most_one(lits, encoding, pool)
