from ecc.curve import P256, Curve25519, Point
from ecc.key import gen_keypair
from ecc.cipher import ElGamal

plain_text = b'This-is-test-plaintext'

pri_key, pub_key = gen_keypair(Curve25519)

cipher_elg = ElGamal(Curve25519)

C1, C2 = cipher_elg.encrypt(plain_text, pub_key)

new_plaintext = cipher_elg.decrypt(pri_key, C1, C2)

print(plain_text == new_plaintext)
