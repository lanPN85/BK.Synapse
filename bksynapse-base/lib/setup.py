import os
import platform
import sys
from setuptools import setup, find_packages

requirements = [
    'marshmallow>=2.19.0',
    'toml>=0.10.0',
    'pymongo>=3.7.2',
    'psutil>=5.6.1',
    'gputil>=1.4.0',
    'python-dateutil>=2.8.0',
    'tensorboardX>=1.6',
    'logzero>=1.5.0',
    'file_read_backwards>=2.0.0'
]

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
