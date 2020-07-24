#!/usr/bin/env python
"""Setup script for the TokenType package"""

import codecs
import setuptools
import tde

setuptools.setup(
    # general description
    name='tde',
    description='Evaluation toolbox for Term Discovery systems',
    version=tde.__version__,
    long_description=open('README.md').read(),
    url='https://github.com/bootphon/tde',
    license='LICENSE.txt',

    # python package dependencies
    setup_requires=['pandas',
                    'numpy'],
    install_requires=['editdistance',
                      'joblib',
                    'intervaltree'],

    tests_require=['pytest'],

    # packages for code and data
    packages=setuptools.find_packages(),
    package_data={'tde': ['share/*']},

    # metadata for upload to PyPI
    author='Julien Karadayi, INRIA',
    author_email='julien.karadayi@inria.fr',
    zip_safe=True,
)
