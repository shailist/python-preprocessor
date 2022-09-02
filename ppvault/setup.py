from setuptools import setup
from distutils.sysconfig import get_python_lib
import sys
import os

SITE_PACKAGES = get_python_lib().split(sys.prefix + os.sep)[1]

setup(
    name='ppvault',
    packages=['ppvault'],
    data_files=[(SITE_PACKAGES, ['ppvault_codec.pth'])]
)
