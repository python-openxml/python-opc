# -*- coding: utf-8 -*-
#
# pkgwriter.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides a low-level, write-only API to a serialized Open Packaging
Convention (OPC) package, essentially an implementation of OpcPackage.save()
"""


class PackageWriter(object):
    """
    Writes a zip-format OPC package to *pkg_file*, where *pkg_file* can be
    either a path to a zip file (a string) or a file-like object. Its single
    API method, :meth:`write`, is static, so this class is not intended to
    be instantiated.
    """
    @staticmethod
    def write(pkg_file, pkg_rels, parts):
        """
        Write a physical package (.pptx file) to *pkg_file* containing
        *pkg_rels* and *parts* and a content types stream based on the
        content types of the parts.
        """
