#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = '0.9.1'

setup(
    name='utilspy',
    version=VERSION,
    author='prior',
    author_email='mprior@hubspot.com',
    packages=find_packages(),
    url='https://github.com/HubSpot/utilspy',
    download_url='https://github.com/HubSpot/utilspy/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description="A number of useful utilities that don't seem to exist elsewhere",
    long_description=open('README.rst').read(),
    install_requires=[],
    platforms=['any']
)

