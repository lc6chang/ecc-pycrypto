import unittest

from ecc import math_utils


SMALL_PRIME = 97
BIG_PRIME = 2 ** 521 - 1


class TestCaseModsqrt(unittest.TestCase):
    def test_small_prime_exist(self):
        self.assertIn(math_utils.modsqrt(24, SMALL_PRIME), [11, SMALL_PRIME - 11])
        self.assertIn(math_utils.modsqrt(4, SMALL_PRIME), [2, SMALL_PRIME - 2])
        self.assertIn(math_utils.modsqrt(18, SMALL_PRIME), [42, SMALL_PRIME - 42])
        self.assertIn(math_utils.modsqrt(1, SMALL_PRIME), [1, SMALL_PRIME - 1])
        self.assertIn(
            math_utils.modsqrt(99999 * SMALL_PRIME + 1, SMALL_PRIME),
            [1, SMALL_PRIME - 1],
        )

    def test_small_prime_not_exist(self):
        self.assertEqual(math_utils.modsqrt(92, SMALL_PRIME), 0)

    def test_big_prime_exist(self):
        self.assertIn(math_utils.modsqrt(361, BIG_PRIME), [19, BIG_PRIME - 19])
        self.assertIn(math_utils.modsqrt(998001, BIG_PRIME), [999, BIG_PRIME - 999])
        self.assertIn(
            math_utils.modsqrt(2 ** 517, BIG_PRIME), [2 ** 519, BIG_PRIME - 2 ** 519]
        )

    def test_big_prime_not_exist(self):
        self.assertEqual(math_utils.modsqrt(2 ** 130 + 2 ** 131, BIG_PRIME), 0)


class TestCaseModinv(unittest.TestCase):
    def test_small_prime_exist(self):
        self.assertEqual(math_utils.modinv(-1000, SMALL_PRIME), 42)
        self.assertEqual(math_utils.modinv(55, SMALL_PRIME), 30)
        self.assertEqual(math_utils.modinv(1000, SMALL_PRIME), 55)

    def test_big_prime_exist(self):
        self.assertEqual(math_utils.modinv(-2 ** 522, BIG_PRIME), 2 ** 520 - 1)
        self.assertEqual(math_utils.modinv(2 ** 485, BIG_PRIME), 68719476736)
        self.assertEqual(math_utils.modinv(2 ** 555, BIG_PRIME), 2 ** 487)
