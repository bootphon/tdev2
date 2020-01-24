#!/usr/bin/env python
"""Setup script for the TokenType package"""

import codecs
import setuptools


setuptools.setup(
    # general description
    name='WDE',
    description='Evaluation toolbox for Word Discovery systems',

    # python package dependencies
    setup_requires=['editdistance',
                    'intervaltree',
                    'pandas >= 0.13.1',
                    'numpy >= 1.8.0',
                    'pytest-runner'],
    tests_require=['pytest>=2.6'],

    # packages for code and data
    packages=setuptools.find_packages(),
    package_data={'WDE': ['share/*']},

    # metadata for upload to PyPI
    author='Julien Karadayi, INRIA',
    author_email='julien.karadayi@inria.fr',
    license='GPL3',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    zip_safe=True,
)
