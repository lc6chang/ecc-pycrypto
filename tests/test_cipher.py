import unittest

from ecc.curve import (
    P256, secp256k1, Curve25519, M383, E222, E382
)
from ecc.cipher import ElGamal
from ecc.key import gen_keypair


CURVES = [P256, secp256k1, Curve25519, M383, E222, E382]
PLAINTEXT = b"I am plaintext."


class ElGamalTestCase(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        for curve in CURVES:
            with self.subTest(curve=curve):
                pri_key, pub_key = gen_keypair(curve)
                cipher_elg = ElGamal(curve)
                C1, C2 = cipher_elg.encrypt(PLAINTEXT, pub_key)
                plaintext = cipher_elg.decrypt(pri_key, C1, C2)
                self.assertEqual(plaintext, PLAINTEXT)

    def test_additive_homomorphism_encryption(self):
        for curve in CURVES:
            with self.subTest(curve=curve):
                pri_key, pub_key = gen_keypair(curve)
                cipher_elg = ElGamal(curve)
                plaintext1 = curve.G * 123
                plaintext2 = curve.G * 456
                C1, C2 = cipher_elg.encrypt_point(plaintext1, pub_key)
                C3, C4 = cipher_elg.encrypt_point(plaintext2, pub_key)
                plaintext = cipher_elg.decrypt_point(pri_key, C1 + C3, C2 + C4)
                self.assertEqual(plaintext, plaintext1 + plaintext2)
