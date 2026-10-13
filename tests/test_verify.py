import unittest
from nqueens.verify import is_valid


class TestVerify(unittest.TestCase):
    def test_valid_solution(self):
        self.assertTrue(is_valid(8, [0, 4, 7, 5, 2, 6, 1, 3]))

    def test_same_column(self):
        self.assertFalse(is_valid(4, [1, 1, 3, 0]))

    def test_same_diagonal(self):
        self.assertFalse(is_valid(4, [0, 1, 3, 2]))

    def test_wrong_length_or_range(self):
        self.assertFalse(is_valid(4, [1, 3, 0]))
        self.assertFalse(is_valid(4, [1, 3, 0, 4]))
        self.assertFalse(is_valid(4, None))


if __name__ == "__main__":
    unittest.main()
