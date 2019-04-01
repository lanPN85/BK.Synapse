import os
import platform
import sys
from setuptools import setup, find_packages

with open('requirements.txt', 'rt') as f:
    requirements = f.readlines()
    requirements = list(map(lambda x: x.strip(), requirements))

VERSION = '0.1.0'

setup(
        name="bksyn",
        version=VERSION,
        description="Shared library for BK.Synapse",
        url="https://github.com/lanPN85/BK.Synapse",
        author="Phan Ngoc Lan",
        author_email="phan.ngoclan58@gmail.com",
        license="",
        packages=find_packages(),
        install_requires=requirements
)
