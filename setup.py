#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = '0.11.1'

setup(
    name='grabbag',
    version=VERSION,
    author='prior',
    author_email='mprior@hubspot.com',
    packages=find_packages(),
    url='https://github.com/HubSpot/grabbag',
    download_url='https://github.com/HubSpot/grabbag/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description="A number of useful utilities that don't seem to exist elsewhere",
    long_description=open('README.rst').read(),
    install_requires=[
        'sanetime>=4,<5'
        ],
    platforms=['any']
)

