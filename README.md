# ecc-pycrypto
This Python package provides simple and user-friendly implementation of ECC, supporting ElGamal encryption, ECDH and ECDSA algorithms.

## Introduction

+ [Elliptic-curve cryptography (ECC)](https://en.wikipedia.org/wiki/Elliptic_curve_cryptography) is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields.
  + [SafeCurves](https://safecurves.cr.yp.to/) provides a list of safe elliptic curves.
  + The three common types of elliptic curves are: [Weierstrass Curve](https://en.wikipedia.org/wiki/Elliptic_curve), [Montgomery Curve](https://en.wikipedia.org/wiki/Montgomery_curve) and [Twisted Edwards Curve](https://en.wikipedia.org/wiki/Twisted_Edwards_curve).

+ [ElGamal encryption](https://en.wikipedia.org/wiki/ElGamal_encryption) is a public-key cryptosystem that enables secure communication between two parties. The ElGamal elliptic curve variant can be explored further in the paper [Architectural Evaluation of Algorithms RSA, ECC and MQQ in Arm Processors](https://www.researchgate.net/publication/269672660_Architectural_Evaluation_of_Algorithms_RSA_ECC_and_MQQ_in_Arm_Processors).

+ [Elliptic Curve Diffie–Hellman (ECDH)](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman) is a key agreement protocol that allows two parties, each having an elliptic-curve public–private key pair, to establish a shared secret over an insecure channel.

+ [Elliptic Curve Digital Signature Algorithm (ECDSA)](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) offers a variant of the [Digital Signature Algorithm (DSA)](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm) which uses elliptic-curve cryptography.

## Warning

This project is intended as an educational tool to help you learn and understand the concepts of ECC and how the algorithm works. **Do not use it in production environments!**


## Installation

```bash
git clone git@github.com:lc6chang/ecc-pycrypto.git
cd ecc-pycrypto
pip3 install .
```

or

```bash
pip3 install git+https://github.com/lc6chang/ecc-pycrypto.git
```

## Usages

### Elliptic curve operations

```python
from ecc import curve, registry

# Choose a curve from registry
P256 = registry.P256
# Define a point on the curve
P = curve.AffinePoint(
    curve=P256,
    x=0x9d8b7f25322574b60f9914b240d79bf35ba7284d0c93a0b76acac49b931cbde6,
    y=0x2aae8628ed337a97cecead2e61d0c188a979a4d1383382a3696b29b449072069,
)
# The base point
G = P256.G  # AffinePoint(curve=P256, x=484395..., y=361342...)
# The neutral point
O = P256.O  # InfinityPoint(curve=P256)
# Operations
assert P + O == P
assert P - P == O
assert 100 * O == O
assert P + P == 2 * P
print(20 * P - 5 * G)  # >>> AffinePoint(curve=P256, x=280875..., y=737429...)
# Define a custom curve
MY_CURVE = curve.ShortWeierstrassCurve(
    name="MY_CURVE",
    a=...,
    b=...,
    p=...,
    n=...,
    G_x=...,
    G_y=...,
)
```


### ElGamal encryption

```python
from ecc import curve, registry, key, cipher

# Plaintext bytes
plaintext_bytes = b"I am plaintext."
# Generate a key pair
pri_key, pub_key = key.gen_key_pair(registry.Curve25519)
# Encode plaintext bytes into a point on the curve
plaintext_point = curve.encode(plaintext_bytes, registry.Curve25519)
# Encrypt using ElGamal algorithm
C1, C2 = cipher.elgamal_encrypt(plaintext_point, pub_key)
# Decrypt
plaintext_point_decrypted = cipher.elgamal_decrypt(pri_key, C1, C2)
# Decode the decrypted point back to plaintext bytes
plaintext_bytes_decrypted = curve.decode(plaintext_point_decrypted)
# Verify
assert plaintext_bytes_decrypted == plaintext_bytes
```

### ECDH shared secret

```python
from ecc import registry, key, cipher

alice_pri_key, alice_pub_key = key.gen_key_pair(registry.Curve25519)
bob_pri_key, bob_pub_key = key.gen_key_pair(registry.Curve25519)
alice_shared = cipher.ecdh_shared(alice_pri_key, bob_pub_key)
bob_shared = cipher.ecdh_shared(bob_pri_key, alice_pub_key)
assert alice_shared == bob_shared
```

### ECDSA sign and verify

```python
from ecc import registry, key, cipher

plaintext_bytes = b"I am plaintext."
pri_key, pub_key = key.gen_key_pair(registry.Curve25519)
signature = cipher.ecdsa_sign(plaintext_bytes, pri_key, registry.Curve25519)
assert cipher.ecdsa_verify(plaintext_bytes, signature, pub_key)
assert not cipher.ecdsa_verify(plaintext_bytes[:-1], signature, pub_key)
```

