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

from opc.phys_pkg import PhysPkgWriter


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
        phys_writer = PhysPkgWriter(pkg_file)
        PackageWriter._write_content_types_stream(phys_writer, parts)
        PackageWriter._write_pkg_rels(phys_writer, pkg_rels)
        PackageWriter._write_parts(phys_writer, parts)
        phys_writer.close()

    @staticmethod
    def _write_content_types_stream(phys_writer, parts):
        """
        Write ``[Content_Types].xml`` part to the physical package with an
        appropriate content type lookup target for each part in *parts*.
        """
        raise NotImplementedError()

    @staticmethod
    def _write_parts(phys_writer, parts):
        """
        Write the blob of each part in *parts* to the package, along with a
        rels item for its relationships if and only if it has any.
        """
        raise NotImplementedError()

    @staticmethod
    def _write_pkg_rels(phys_writer, pkg_rels):
        """
        Write the XML rels item for *pkg_rels* ('/_rels/.rels') to the
        package.
        """
        raise NotImplementedError()
