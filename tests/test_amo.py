import unittest

from pysat.solvers import Solver

from nqueens.amo import ENCODINGS, VarPool, at_most_one, exactly_one


def satisfiable(clauses, assumptions):
    with Solver(name="cadical195", bootstrap_with=clauses) as s:
        return s.solve(assumptions=assumptions)


def assignment(lits, mask):
    assumptions = []
    count = 0
    for i in range(len(lits)):
        if (mask // 2 ** i) % 2 == 1:
            assumptions.append(lits[i])
            count += 1
        else:
            assumptions.append(-lits[i])
    return assumptions, count


# thử mọi cách gán cho n = 1..7 biến
class TestAmo(unittest.TestCase):
    def test_at_most_one(self):
        for name in ENCODINGS:
            for n in range(1, 8):
                lits = list(range(1, n + 1))
                clauses = at_most_one(lits, name, VarPool(n))
                for mask in range(2 ** n):
                    assumptions, count = assignment(lits, mask)
                    self.assertEqual(satisfiable(clauses, assumptions), count <= 1, (name, n, mask))

    def test_exactly_one(self):
        for name in ENCODINGS:
            for n in range(1, 8):
                lits = list(range(1, n + 1))
                clauses = exactly_one(lits, name, VarPool(n))
                for mask in range(2 ** n):
                    assumptions, count = assignment(lits, mask)
                    self.assertEqual(satisfiable(clauses, assumptions), count == 1, (name, n, mask))

    def test_binary_size(self):
        for n, k in [(2, 1), (3, 2), (4, 2), (5, 3), (8, 3), (9, 4)]:
            pool = VarPool(n)
            clauses = at_most_one(list(range(1, n + 1)), "binary", pool)
            self.assertEqual(pool.top - n, k)
            self.assertEqual(len(clauses), n * k)

    def test_seqcounter_size(self):
        for n in range(2, 10):
            pool = VarPool(n)
            clauses = at_most_one(list(range(1, n + 1)), "seqcounter", pool)
            self.assertEqual(pool.top - n, n - 1)
            self.assertEqual(len(clauses), 3 * n - 4)


if __name__ == "__main__":
    unittest.main()
