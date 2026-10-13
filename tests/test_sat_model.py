import unittest

from nqueens.sat_model import count_solutions, encode, lines, solve
from nqueens.verify import is_valid

# Số lời giải với N = 1..9 (OEIS A000170)
KNOWN_COUNTS = [1, 0, 0, 2, 10, 4, 40, 92, 352]


class TestSatModel(unittest.TestCase):
    def test_lines(self):
        rows, cols, diags, anti_diags = lines(4)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(cols), 4)
        self.assertEqual(len(diags), 7)
        self.assertEqual(len(anti_diags), 7)
        # mỗi ô nằm trên đúng một hàng, một cột, một đường chéo mỗi loại
        for group in (rows, cols, diags, anti_diags):
            self.assertEqual(sorted(v for line in group for v in line), list(range(1, 17)))

    def test_binomial_uses_only_cell_variables(self):
        self.assertEqual(encode(8).nv, 64)

    def test_solutions_are_valid(self):
        for n in [1] + list(range(4, 31)):
            self.assertTrue(is_valid(n, solve(n)), n)

    def test_no_solution(self):
        self.assertIsNone(solve(2))
        self.assertIsNone(solve(3))

    def test_count_solutions(self):
        for n, expected in enumerate(KNOWN_COUNTS, start=1):
            self.assertEqual(count_solutions(n), expected, n)


if __name__ == "__main__":
    unittest.main()
