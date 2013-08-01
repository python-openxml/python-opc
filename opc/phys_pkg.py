# -*- coding: utf-8 -*-
#
# phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides a general interface to a *physical* OPC package, such as a zip file.
"""


class PhysPkgReader(object):
    """
    Factory for physical package reader objects.
    """
    def __new__(cls, pkg_file):
        return ZipPkgReader(pkg_file)


class ZipPkgReader(object):
    """
    Implements |PhysPkgReader| interface for a zip file OPC package.
    """
