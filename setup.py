import setuptools


VERSION = "2.0.0"

setuptools.setup(
    name="ecc_pycrypto",
    version=VERSION,
    author="lc6chang",
    author_email="lc6chang@gmail.com",
    url="https://github.com/lc6chang/ecc-pycrypto",
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires=">=3.10"
)
