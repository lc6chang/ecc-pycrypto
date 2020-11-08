from ecc.curve import E382
from ecc.key import gen_keypair
from ecc.cipher import ElGamal

plain_text = b"This-is-test-plaintext"

pri_key, pub_key = gen_keypair(E382)

cipher_elg = ElGamal(E382)

C1, C2 = cipher_elg.encrypt(plain_text, pub_key)

new_plaintext = cipher_elg.decrypt(pri_key, C1, C2)

print(plain_text == new_plaintext)
