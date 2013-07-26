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

from zipfile import ZIP_DEFLATED, ZipFile


class PhysPkgReader(object):
    """
    Factory for physical package reader objects.
    """
    def __new__(cls, pkg_file):
        return ZipPkgReader(pkg_file)


class PhysPkgWriter(object):
    """
    Factory for physical package writer objects.
    """
    def __new__(cls, pkg_file):
        return ZipPkgWriter(pkg_file)


class ZipPkgReader(object):
    """
    Implements |PhysPkgReader| interface for a zip file OPC package.
    """
    _CONTENT_TYPES_MEMBERNAME = '[Content_Types].xml'

    def __init__(self, pkg_file):
        super(ZipPkgReader, self).__init__()
        self._zipf = ZipFile(pkg_file, 'r')

    def blob_for(self, pack_uri):
        """
        Return blob corresponding to *pack_uri*. Raises |ValueError| if no
        matching member is present in zip archive.
        """
        return self._zipf.read(pack_uri.membername)

    def close(self):
        """
        Close the zip archive, releasing any resources it is using.
        """
        self._zipf.close()

    @property
    def content_types_xml(self):
        """
        Return the `[Content_Types].xml` blob from the zip package.
        """
        return self._zipf.read(self._CONTENT_TYPES_MEMBERNAME)

    def rels_xml_for(self, source_uri):
        """
        Return rels item XML for source with *source_uri* or None if no rels
        item is present.
        """
        try:
            rels_xml = self._zipf.read(source_uri.rels_uri.membername)
        except KeyError:
            rels_xml = None
        return rels_xml


class ZipPkgWriter(object):
    """
    Implements |PhysPkgWriter| interface for a zip file OPC package.
    """
    def __init__(self, pkg_file):
        super(ZipPkgWriter, self).__init__()
        self._zipf = ZipFile(pkg_file, 'w', compression=ZIP_DEFLATED)

    def close(self):
        """
        Close the zip archive, flushing any pending physical writes and
        releasing any resources it's using.
        """
        self._zipf.close()

    def write(self, pack_uri, blob):
        """
        Write *blob* to this zip package with the membername corresponding to
        *pack_uri*.
        """
        self._zipf.writestr(pack_uri.membername, blob)
