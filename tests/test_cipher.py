import unittest
import os
import random

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


class TestCaseElGamal(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                pri_key, pub_key = key.gen_key_pair(curve_)
                plaintext_len = random.randint(0, 20)
                plaintext_bytes = os.urandom(plaintext_len)
                plaintext = curve.encode(plaintext_bytes, curve_)
                C1, C2 = cipher.elgamal_encrypt(plaintext, pub_key)
                plaintext_decrypted = cipher.elgamal_decrypt(pri_key, C1, C2)
                plaintext_decrypted_bytes = curve.decode(plaintext_decrypted)
                self.assertEqual(plaintext_decrypted_bytes, plaintext_bytes)

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


class TestCaseEcdh(unittest.TestCase):
    def test_ecdh_shared(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                alice_pri_key, alice_pub_key = key.gen_key_pair(curve_)
                bob_pri_key, bob_pub_key = key.gen_key_pair(curve_)
                alice_shared = cipher.ecdh_shared(alice_pri_key, bob_pub_key)
                bob_shared = cipher.ecdh_shared(bob_pri_key, alice_pub_key)
                self.assertEqual(alice_shared, bob_shared)


class TestEcdsa(unittest.TestCase):
    def test_ecdsa_valid(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                plaintext_bytes = os.urandom(128)
                pri_key, pub_key = key.gen_key_pair(curve_)
                signature = cipher.ecdsa_sign(plaintext_bytes, pri_key, curve_,)
                verify = cipher.ecdsa_verify(plaintext_bytes, signature, pub_key)
                self.assertTrue(verify)

    def test_ecdsa_invalid(self):
        for curve_ in CURVES:
            with self.subTest(name=curve_.name):
                plaintext_bytes = os.urandom(128)
                pri_key, pub_key = key.gen_key_pair(curve_)
                signature = cipher.ecdsa_sign(plaintext_bytes, pri_key, curve_,)
                verify = cipher.ecdsa_verify(plaintext_bytes[:-1], signature, pub_key)
                self.assertFalse(verify)
