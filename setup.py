#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


if sys.platform == "win32":
    install_requires = [
        "pywinusb"
    ]
else:
    install_requires = [
        "pyusb>=1.0.0"
    ]

setup_options = dict(
    name='blinkstick',
    version=find_version("blinkstick", "__version__.py"),
    description='Python package to control BlinkStick USB devices.',
    long_description=read('README.rst'),
    author='Arvydas Juskevicius',
    author_email='arvydas@arvydas.co.uk',
    url='http://pypi.python.org/pypi/BlinkStick/',
    scripts=['bin/blinkstick'],
    packages=find_packages(exclude=['tests*']),
    install_requires=install_requires,
    license="LICENSE.txt",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

setup(**setup_options)

