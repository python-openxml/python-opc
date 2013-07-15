#!/usr/bin/env python

import os
import re

from setuptools import setup

# Read the version from opc.__version__ without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
thisdir = os.path.dirname(__file__)
init_py_path = os.path.join(thisdir, 'opc', '__init__.py')
version = re.search("__version__ = '([^']+)'",
                    open(init_py_path).read()).group(1)


NAME = 'python-opc'
VERSION = version
DESCRIPTION = (
    'Manipulate Open Packaging Convention (OPC) files, e.g. .docx, .pptx, an'
    'd .xlsx files for Microsoft Office'
)
KEYWORDS = 'opc open xml docx pptx xslx office'
AUTHOR = 'Steve Canny'
AUTHOR_EMAIL = 'python-opc@googlegroups.com'
URL = 'https://github.com/python-openxml/python-opc'
LICENSE = 'MIT'
PACKAGES = ['opc']

INSTALL_REQUIRES = ['lxml']
TEST_SUITE = 'test'
TESTS_REQUIRE = ['behave', 'mock', 'pytest']

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme).read()


params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'long_description': LONG_DESCRIPTION,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          LICENSE,
    'packages':         PACKAGES,
    'install_requires': INSTALL_REQUIRES,
    'tests_require':    TESTS_REQUIRE,
    'test_suite':       TEST_SUITE,
    'classifiers':      CLASSIFIERS,
}

setup(**params)
