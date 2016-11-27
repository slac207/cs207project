#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for timeseries.

    This file was generated with PyScaffold 2.5.6, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['six', 'pyscaffold>=2.5a0,<2.6a0'] + sphinx,
          use_pyscaffold=True)

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='coveralls',
    version='1.1',
    packages=['coveralls'],
    url='http://github.com/coagulant/coveralls-python',
    license='MIT',
    author='Ilya Baryshev',
    author_email='baryshev@gmail.com',
    description='Show coverage stats online via coveralls.io',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    entry_points={
        'console_scripts': [
            'coveralls = coveralls.cli:main',
        ],
    },
    install_requires=['docopt>=0.6.1', 'coverage>=3.6', 'requests>=1.0.0'],
    tests_require=['mock', 'pytest>=2.7.3,<2.8', 'sh>=1.08'],
    extras_require={
        'yaml': ['PyYAML>=3.10']
    },
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
if __name__ == "__main__":
    setup_package()
