#!/usr/bin/env python
"""Setup script for the TokenType package"""

import codecs
import setuptools


setuptools.setup(
    # general description
    name='TokenType',
    description='Evaluation toolbox for the Token/Type measures',

    # python package dependencies
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # packages for code and data
    packages=setuptools.find_packages(),
    package_data={'TokenType': ['TokenType/*']},

    # metadata for upload to PyPI
    author='Julien Karadayi, INRIA',
    author_email='julien.karadayi@inria.fr',
    license='GPL3',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    zip_safe=True,
)
