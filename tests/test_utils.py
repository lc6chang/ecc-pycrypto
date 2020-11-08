import unittest

from ecc.utils import int_length_in_byte


class IntLengthInBytesTest(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(int_length_in_byte(0), 0)

    def test_positive(self):
        self.assertEqual(int_length_in_byte(1024), 2)
        self.assertEqual(int_length_in_byte(65535), 2)
        self.assertEqual(int_length_in_byte(65536), 3)

    def test_negative(self):
        with self.assertRaises(AssertionError):
            int_length_in_byte(-1)
