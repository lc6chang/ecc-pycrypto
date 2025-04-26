import unittest

from ecc import curve
from ecc import registry
from ecc import cipher
from ecc import key


CURVES: list[curve.Curve] = [
    registry.P256,
    registry.secp256k1,
    registry.Curve25519,
    registry.M383,
    registry.E222,
    registry.E382,
]
PLAINTEXT_BYTES = b"I am plaintext."


class TestCaseElGamal(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                pri_key, pub_key = key.gen_key_pair(curve_)
                plaintext = curve_.encode_point(PLAINTEXT_BYTES)
                C1, C2 = cipher.elgamal_encrypt(plaintext, pub_key)
                plaintext_decrypted = cipher.elgamal_decrypt(pri_key, C1, C2)
                plaintext_decrypted_bytes = curve_.decode_point(plaintext_decrypted)
                self.assertEqual(plaintext_decrypted_bytes, PLAINTEXT_BYTES)

    def test_additive_homomorphism_encryption(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                pri_key, pub_key = key.gen_key_pair(curve_)
                plaintext1 = curve_.G * 123
                plaintext2 = curve_.G * 456
                C1, C2 = cipher.elgamal_encrypt(plaintext1, pub_key)
                C3, C4 = cipher.elgamal_encrypt(plaintext2, pub_key)
                plaintext = cipher.elgamal_decrypt(pri_key, C1 + C3, C2 + C4)
                self.assertEqual(plaintext, plaintext1 + plaintext2)
