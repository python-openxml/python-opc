# -*- coding: utf-8 -*-
#
# pkgreader.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides a low-level, read-only API to a serialized Open Packaging Convention
(OPC) package.
"""


class PackageReader(object):
    """
    Provides access to the contents of a zip-format OPC package via its
    :attr:`serialized_parts` and :attr:`pkg_srels` attributes.
    """
    @staticmethod
    def from_file(pkg_file):
        """
        Return a |PackageReader| instance loaded with contents of *pkg_file*.
        """
