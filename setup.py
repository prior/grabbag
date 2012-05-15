#!/usr/bin/env python
from distutils.core import setup

VERSION = '0.8.1'

setup(
    name='utilspy',
    version=VERSION,
    description='Random useful python utilities that don\'t seem to exist elsewhere',
    long_description = open('README.rst').read(),
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    url='https://github.com/prior/utilspy',
    download_url='https://github.com/prior/utilspy/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    packages=['utils','utils.test'],
    install_requires=[ 'nose==1.1.2' ]
)
