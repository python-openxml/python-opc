# -*- coding: utf-8 -*-
#
# package.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides an API for manipulating Open Packaging Convention (OPC) packages.
"""

from opc.packuri import PACKAGE_URI
from opc.pkgreader import PackageReader


class OpcPackage(object):
    """
    Main API class for |python-opc|. A new instance is constructed by calling
    the :meth:`open` class method with a path to a package file or file-like
    object containing one.
    """
    def __init__(self):
        super(OpcPackage, self).__init__()
        self._rels = RelationshipCollection(PACKAGE_URI.baseURI)

    @staticmethod
    def open(pkg_file):
        """
        Return an |OpcPackage| instance loaded with the contents of
        *pkg_file*.
        """
        pkg = OpcPackage()
        pkg_reader = PackageReader.from_file(pkg_file)
        Unmarshaller.unmarshal(pkg_reader, pkg, PartFactory)
        return pkg

    @property
    def rels(self):
        """
        Return a reference to the |RelationshipCollection| holding the
        relationships for this package.
        """
        return self._rels


class Part(object):
    """
    Base class for package parts. Provides common properties and methods, but
    intended to be subclassed in client code to implement specific part
    behaviors.
    """
    def __init__(self, partname, content_type, blob):
        super(Part, self).__init__()
        self._partname = partname
        self._content_type = content_type
        self._blob = blob

    @property
    def blob(self):
        """
        Contents of this package part as a sequence of bytes. May be text or
        binary.
        """
        return self._blob

    @property
    def content_type(self):
        """
        Content type of this part.
        """
        return self._content_type

    @property
    def partname(self):
        """
        |PackURI| instance containing partname for this part.
        """
        return self._partname

    def _after_unmarshal(self):
        """
        Entry point for post-unmarshaling processing, for example to parse
        the part XML. May be overridden by subclasses without forwarding call
        to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass


class PartFactory(object):
    """
    Provides a way for client code to specify a subclass of |Part| to be
    constructed by |Unmarshaller| based on its content type.
    """
    def __new__(cls, partname, content_type, blob):
        return Part(partname, content_type, blob)


class RelationshipCollection(object):
    """
    Collection object for |_Relationship| instances, having list semantics.
    """
    def __init__(self, baseURI):
        super(RelationshipCollection, self).__init__()
        self._rels = []

    def __len__(self):
        """Implements len() built-in on this object"""
        return self._rels.__len__()


class Unmarshaller(object):
    """
    Hosts static methods for unmarshalling a package from a |PackageReader|
    instance.
    """
    @staticmethod
    def unmarshal(pkg_reader, pkg, part_factory):
        """
        Construct graph of parts and realized relationships based on the
        contents of *pkg_reader*, delegating construction of each part to
        *part_factory*. Package relationships are added to *pkg*.
        """
        parts = Unmarshaller._unmarshal_parts(pkg_reader, part_factory)
        Unmarshaller._unmarshal_relationships(pkg_reader, pkg, parts)
        for part in parts.values():
            part._after_unmarshal()

    @staticmethod
    def _unmarshal_parts(pkg_reader, part_factory):
        """
        Return a dictionary of |Part| instances unmarshalled from
        *pkg_reader*, keyed by partname. Side-effect is that each part in
        *pkg_reader* is constructed using *part_factory*.
        """
        parts = {}
        for partname, content_type, blob in pkg_reader.iter_sparts():
            parts[partname] = part_factory(partname, content_type, blob)
        return parts

    @staticmethod
    def _unmarshal_relationships(pkg_reader, pkg, parts):
        """
        Add a relationship to the source object corresponding to each of the
        relationships in *pkg_reader* with its target_part set to the actual
        target part in *parts*.
        """
        for source_uri, srel in pkg_reader.iter_srels():
            source = pkg if source_uri == '/' else parts[source_uri]
            target = (srel.target_ref if srel.is_external
                      else parts[srel.target_partname])
            source._add_relationship(srel.reltype, target, srel.rId,
                                     srel.is_external)
