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

from opc.packuri import PACKAGE_URI
from opc.phys_pkg import PhysPkgReader


class PackageReader(object):
    """
    Provides access to the contents of a zip-format OPC package via its
    :attr:`serialized_parts` and :attr:`pkg_srels` attributes.
    """
    def __init__(self, content_types, pkg_srels, sparts):
        super(PackageReader, self).__init__()
        self._sparts = sparts

    @staticmethod
    def from_file(pkg_file):
        """
        Return a |PackageReader| instance loaded with contents of *pkg_file*.
        """
        phys_reader = PhysPkgReader(pkg_file)
        content_types = _ContentTypeMap.from_xml(phys_reader.content_types_xml)
        pkg_srels = PackageReader._srels_for(phys_reader, PACKAGE_URI)
        sparts = PackageReader._load_serialized_parts(phys_reader, pkg_srels,
                                                      content_types)
        phys_reader.close()
        return PackageReader(content_types, pkg_srels, sparts)

    def iter_sparts(self):
        """
        Generate a 3-tuple `(partname, content_type, blob)` for each of the
        serialized parts in the package.
        """
        for spart in self._sparts:
            yield (spart.partname, spart.content_type, spart.blob)

    @staticmethod
    def _load_serialized_parts(phys_reader, pkg_srels, content_types):
        """
        Return a list of |_SerializedPart| instances corresponding to the
        parts in *phys_reader* accessible by walking the relationship graph
        starting with *pkg_srels*.
        """

    @staticmethod
    def _srels_for(phys_reader, source_uri):
        """
        Return |_SerializedRelationshipCollection| instance populated with
        relationships for source identified by *source_uri*.
        """


class _ContentTypeMap(object):
    """
    Value type providing dictionary semantics for looking up content type by
    part name, e.g. ``content_type = cti['/ppt/presentation.xml']``.
    """
    @staticmethod
    def from_xml(content_types_xml):
        """
        Return a new |_ContentTypeMap| instance populated with the contents
        of *content_types_xml*.
        """
