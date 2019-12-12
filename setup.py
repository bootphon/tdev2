#!/usr/bin/env python
"""Setup script for the TokenType package"""

import codecs
import setuptools


setuptools.setup(
    # general description
    name='WDE',
    description='Evaluation toolbox for Word Discovery systems',

    # python package dependencies
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # packages for code and data
    packages=setuptools.find_packages(),
    package_data={'WDE': ['WDE/share/*']},

    # metadata for upload to PyPI
    author='Julien Karadayi, INRIA',
    author_email='julien.karadayi@inria.fr',
    license='GPL3',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    zip_safe=True,
)
