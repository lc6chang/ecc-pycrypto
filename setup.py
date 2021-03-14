from setuptools import setup, find_namespace_packages

from ecc import __version__

dependencies = [
    "dataclasses",
]

setup(
    name="ecc-pycrypto",
    author="lc6chang",
    author_email="lc6chang@gmail.com",
    version=__version__,
    packages=find_namespace_packages(),
    install_requires=dependencies,
    python_requires=">=3.6"
)
