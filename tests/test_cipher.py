import unittest

from ecc.curve import (
    P256, secp256k1, Curve25519, M383, E222, E382
)
from ecc.cipher import ElGamal
from ecc.key import gen_keypair


CURVES = [P256, secp256k1, Curve25519, M383, E222, E382]
PLAIN_TEXT = b"This is a plain text."


class ElGamalTestCase(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        for curve in CURVES:
            with self.subTest(curve=curve):
                pri_key, pub_key = gen_keypair(curve)
                cipher_elg = ElGamal(curve)
                C1, C2 = cipher_elg.encrypt(PLAIN_TEXT, pub_key)
                plain_text = cipher_elg.decrypt(pri_key, C1, C2)
                self.assertEqual(plain_text, PLAIN_TEXT)
