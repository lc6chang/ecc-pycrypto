# ecc-pycrypto
This is a Python package for ECC and ElGamal elliptic curve encryption.

## Introduction

+ [ElGamal encryption](https://en.wikipedia.org/wiki/ElGamal_encryption) is a public-key cryptosystem. It uses asymmetric key encryption for communicating between two parties and encrypting the message.

+ [Elliptic-curve cryptography (ECC)](https://en.wikipedia.org/wiki/Elliptic_curve_cryptography) is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields.
  + [SafeCurves](https://safecurves.cr.yp.to/) shows us the safety Elliptic curve.
  + There are three typical curves: [Weierstrass Curve](https://en.wikipedia.org/wiki/Elliptic_curve), [Montgomery Curve](https://en.wikipedia.org/wiki/Montgomery_curve) and [Twisted Edwards Curve](https://en.wikipedia.org/wiki/Twisted_Edwards_curve).

+ For ElGamal elliptic curve crypto, please refer to [Architectural Evaluation of Algorithms RSA, ECC and MQQ in Arm Processors](https://www.researchgate.net/publication/269672660_Architectural_Evaluation_of_Algorithms_RSA_ECC_and_MQQ_in_Arm_Processors).

## Warning

This project only aims to help you learn and understand what is ECC and how the algorithm works. **Do not use is directly in production environment!**

Some cons: The operations of curve points are just implemented in a common way. We don't implement them using [Jacobian Coordinates](https://en.wikibooks.org/wiki/Cryptography/Prime_Curve/Jacobian_Coordinates). Also, we implement them in pure Python. It will be slower than C.

## Installation

```bash
git clone git@github.com:lc6chang/ecc-pycrypto.git
cd ecc-pycrypto
pip3 install .
```

## Usages

### ElGamal elliptic curve encryption and decryption

```python
from ecc.curve import P256
from ecc.key import gen_keypair
from ecc.cipher import ElGamal


# Plaintext
plain_text = b'This-is-test-plaintext'
# Generate key pair
pri_key, pub_key = gen_keypair(Curve25519)
# Encrypt using ElGamal algorithm
cipher_elg = ElGamal(Curve25519)
C1, C2 = cipher_elg.encrypt(plain_text, pub_key)
# Decrypt
new_plaintext = cipher_elg.decrypt(pri_key, C1, C2)
```

## Common elliptic curve

```python
from ecc.curve import P256, Point

P = Point(0x9d8b7f25322574b60f9914b240d79bf35ba7284d0c93a0b76acac49b931cbde6,
          0x2aae8628ed337a97cecead2e61d0c188a979a4d1383382a3696b29b449072069,
          P256)

Q = Point(0x214735e43acb4530348f31bf1d4e5444711c9d9dba9ca30389fd68573c3db138,
          0xdc029894c4b8060fa951d2a7b052c88bf72218b265b2e2c04458ac187cede004,
          P256)

P + Q
P + P
3 * P
Q * 1000 + P
```

```python
from ecc.curve import ShortWeierstrassCurve

# You could also write your own Curve
YOUR_CURVE = ShortWeierstrassCurve(
  name=CURVE_NAME,
  a=A,
  b=B,
  p=P,
  n=N,
  gx=G_X,
  gy=G_Y
)
```

