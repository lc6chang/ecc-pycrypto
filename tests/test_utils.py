import unittest
import os

from ecc import utils


class TestCaseByteLength(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(utils.byte_length(0), 0)

    def test_positive(self):
        self.assertEqual(utils.byte_length(1024), 2)
        self.assertEqual(utils.byte_length(65535), 2)
        self.assertEqual(utils.byte_length(65536), 3)

    def test_negative(self):
        with self.assertRaises(AssertionError):
            utils.byte_length(-1)


class TestCaseRandomNbitsInt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(utils.random_nbits_int(0, os.urandom), 0)

    def test_positive(self):
        self.assertTrue(utils.random_nbits_int(1, os.urandom).bit_length() <= 1)
        self.assertTrue(utils.random_nbits_int(15, os.urandom).bit_length() <= 15)
        self.assertTrue(utils.random_nbits_int(16, os.urandom).bit_length() <= 16)

    def test_negative(self):
        with self.assertRaises(AssertionError):
            utils.random_nbits_int(-1, os.urandom)
