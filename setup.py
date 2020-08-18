import sys

from setuptools import setup

if sys.version_info[0] > 2:
    readme = open("README.md", encoding="utf-8").read()
else:
    readme = open("README.md").read()

setup(
    name="minij",
    version="1.0.0",
    url="https://github.com/betoSolares/minij",
    author="Roberto Solares and Brenner Hernadez",
    license="MIT",
    description="A toy implementation of a compiler written in python",
    long_description=readme,
)

