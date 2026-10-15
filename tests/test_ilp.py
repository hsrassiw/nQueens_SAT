import unittest

from nqueens.ilp import solve_cplex_mip, solve_gurobi
from nqueens.verify import is_valid


class TestIlp(unittest.TestCase):
    def test_cplex_mip(self):
        for n in [1] + list(range(4, 31)):
            self.assertTrue(is_valid(n, solve_cplex_mip(n)), n)
        self.assertIsNone(solve_cplex_mip(2))
        self.assertIsNone(solve_cplex_mip(3))

    def test_gurobi(self):
        for n in [1] + list(range(4, 31)):
            self.assertTrue(is_valid(n, solve_gurobi(n)), n)
        self.assertIsNone(solve_gurobi(2))
        self.assertIsNone(solve_gurobi(3))


if __name__ == "__main__":
    unittest.main()
