from ecc.curve import Curve25519, Point
from ecc.cipher import ElGamal
from ecc.key import gen_keypair

pri_key, pub_key = gen_keypair(Curve25519)
cipher_elg = ElGamal(Curve25519)
plain_text_1: Point = Curve25519.G * 999  # magic number 999, just an example
plain_text_2: Point = Curve25519.G * 777  # magic number 777, just an example
X=C1, C2 = cipher_elg.encrypt_raw(plain_text_1, pub_key)
Y=C3, C4 = cipher_elg.encrypt_raw(plain_text_2, pub_key)
C5 = Curve25519.add_point(C1,C3)
C6 = Curve25519.add_point(C2,C4)
result = cipher_elg.decrypt_raw(pri_key, C5, C6)

print(result == plain_text_1 + plain_text_2)

# >> True
