#!/usr/bin/env python
"""Setup script for the TokenType package"""

import codecs
import setuptools
import tdev2

setuptools.setup(
    # general description
    name='tdev2',
    description='Evaluation toolbox for Term Discovery systems',
    version=tdev2.__version__,
    long_description=open('README.md').read(),
    url='https://github.com/bootphon/tdev2',
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
    package_data={'tdev2': ['share/*']},

    # metadata for upload to PyPI
    author='Julien Karadayi, INRIA',
    author_email='julien.karadayi@inria.fr',
    zip_safe=True,
)
