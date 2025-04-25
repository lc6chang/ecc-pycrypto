import unittest

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
