import unittest
import os

from ecc import utils


class TestCaseRandomNbitsInt(unittest.TestCase):
    def test_positive(self):
        self.assertTrue(utils.random_nbits_int(1, os.urandom).bit_length() <= 1)
        self.assertTrue(utils.random_nbits_int(15, os.urandom).bit_length() <= 15)
        self.assertTrue(utils.random_nbits_int(16, os.urandom).bit_length() <= 16)

    def test_zero_and_negative(self):
        with self.assertRaises(AssertionError):
            utils.random_nbits_int(0, os.urandom)
        with self.assertRaises(AssertionError):
            utils.random_nbits_int(-1, os.urandom)


class TestCaseRandomIntExclusive(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(utils.random_int_exclusive(2, os.urandom), 1)
        self.assertIn(utils.random_int_exclusive(10, os.urandom), list(range(1, 10)))
        self.assertIn(utils.random_int_exclusive(100, os.urandom), list(range(1, 100)))
