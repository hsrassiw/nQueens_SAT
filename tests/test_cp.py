import os
import unittest

from nqueens.cp import CPOPTIMIZER, solve_cplex_cp, solve_cpsat
from nqueens.verify import is_valid


class TestCpSat(unittest.TestCase):
    def test_solutions_are_valid(self):
        for n in [1] + list(range(4, 31)):
            self.assertTrue(is_valid(n, solve_cpsat(n)), n)

    def test_no_solution(self):
        self.assertIsNone(solve_cpsat(2))
        self.assertIsNone(solve_cpsat(3))


# cần cài CPLEX Studio để có cpoptimizer
@unittest.skipUnless(os.path.exists(CPOPTIMIZER), "chưa cài CPLEX CP Optimizer")
class TestCplexCp(unittest.TestCase):
    def test_solutions_are_valid(self):
        for n in [1] + list(range(4, 31)):
            self.assertTrue(is_valid(n, solve_cplex_cp(n)), n)

    def test_no_solution(self):
        self.assertIsNone(solve_cplex_cp(2))
        self.assertIsNone(solve_cplex_cp(3))


if __name__ == "__main__":
    unittest.main()
