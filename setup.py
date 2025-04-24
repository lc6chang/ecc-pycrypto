from setuptools import setup
from setuptools import find_namespace_packages

from ecc import __version__


setup(
    name="ecc-pycrypto",
    author="lc6chang",
    author_email="lc6chang@gmail.com",
    version=__version__,
    packages=find_namespace_packages(),
    install_requires=[],
    python_requires=">=3.7"
)
