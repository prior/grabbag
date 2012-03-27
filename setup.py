#!/usr/bin/env python
from distutils.core import setup

setup(
    name='utilspy',
    version='0.4',
    description='Random useful python utilities that don\'t seem to exist elsewhere',
    long_description = open('README.md').read(),
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    url='https://github.com/prior/utilspy',
    download_url='https://github.com/prior/utilspy/tarball/v0.4',
    license='LICENSE.txt',
    packages=['utils'],
    install_requires=[ 'nose==1.1.2' ]
)
