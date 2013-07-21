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

from opc.constants import RELATIONSHIP_TARGET_MODE as RTM
from opc.oxml import oxml_fromstring
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
        sparts = []
        part_walker = PackageReader._walk_phys_parts(phys_reader, pkg_srels)
        for partname, blob, srels in part_walker:
            content_type = content_types[partname]
            spart = _SerializedPart(partname, content_type, blob, srels)
            sparts.append(spart)
        return tuple(sparts)

    @staticmethod
    def _srels_for(phys_reader, source_uri):
        """
        Return |_SerializedRelationshipCollection| instance populated with
        relationships for source identified by *source_uri*.
        """
        rels_xml = phys_reader.rels_xml_for(source_uri)
        return _SerializedRelationshipCollection.load_from_xml(
            source_uri.baseURI, rels_xml)

    @staticmethod
    def _walk_phys_parts(phys_reader, srels, visited_partnames=None):
        """
        Generate a 3-tuple `(partname, blob, srels)` for each of the parts in
        *phys_reader* by walking the relationship graph rooted at srels.
        """
        if visited_partnames is None:
            visited_partnames = []
        for srel in srels:
            if srel.is_external:
                continue
            partname = srel.target_partname
            if partname in visited_partnames:
                continue
            visited_partnames.append(partname)
            part_srels = PackageReader._srels_for(phys_reader, partname)
            blob = phys_reader.blob_for(partname)
            yield (partname, blob, part_srels)
            for partname, blob, srels in PackageReader._walk_phys_parts(
                    phys_reader, part_srels, visited_partnames):
                yield (partname, blob, srels)


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


class _SerializedPart(object):
    """
    Value object for an OPC package part. Provides access to the partname,
    content type, blob, and serialized relationships for the part.
    """
    def __init__(self, partname, content_type, blob, srels):
        super(_SerializedPart, self).__init__()


class _SerializedRelationship(object):
    """
    Value object representing a serialized relationship in an OPC package.
    Serialized, in this case, means any target part is referred to via its
    partname rather than a direct link to an in-memory |Part| object.
    """
    def __init__(self, baseURI, rel_elm):
        super(_SerializedRelationship, self).__init__()
        self._rId = rel_elm.rId
        self._reltype = rel_elm.reltype
        self._target_mode = rel_elm.target_mode
        self._target_ref = rel_elm.target_ref

    @property
    def is_external(self):
        """
        True if target_mode is ``RTM.EXTERNAL``
        """
        return self._target_mode == RTM.EXTERNAL

    @property
    def reltype(self):
        """Relationship type, like ``RT.OFFICE_DOCUMENT``"""
        return self._reltype

    @property
    def rId(self):
        """
        Relationship id, like 'rId9', corresponds to the ``Id`` attribute on
        the ``CT_Relationship`` element.
        """
        return self._rId

    @property
    def target_mode(self):
        """
        String in ``TargetMode`` attribute of ``CT_Relationship`` element,
        one of ``RTM.INTERNAL`` or ``RTM.EXTERNAL``.
        """
        return self._target_mode

    @property
    def target_ref(self):
        """
        String in ``Target`` attribute of ``CT_Relationship`` element, a
        relative part reference for internal target mode or an arbitrary URI,
        e.g. an HTTP URL, for external target mode.
        """
        return self._target_ref


class _SerializedRelationshipCollection(object):
    """
    Read-only sequence of |_SerializedRelationship| instances corresponding
    to the relationships item XML passed to constructor.
    """
    def __init__(self):
        super(_SerializedRelationshipCollection, self).__init__()
        self._srels = []

    def __iter__(self):
        """Support iteration, e.g. 'for x in srels:'"""
        return self._srels.__iter__()

    @staticmethod
    def load_from_xml(baseURI, rels_item_xml):
        """
        Return |_SerializedRelationshipCollection| instance loaded with the
        relationships contained in *rels_item_xml*. Returns an empty
        collection if *rels_item_xml* is |None|.
        """
        srels = _SerializedRelationshipCollection()
        if rels_item_xml is not None:
            rels_elm = oxml_fromstring(rels_item_xml)
            for rel_elm in rels_elm.Relationship:
                srels._srels.append(_SerializedRelationship(baseURI, rel_elm))
        return srels
