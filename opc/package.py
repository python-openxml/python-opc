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

from opc.oxml import CT_Relationships
from opc.packuri import PACKAGE_URI
from opc.pkgreader import PackageReader
from opc.pkgwriter import PackageWriter


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
    def parts(self):
        """
        Return an immutable sequence (tuple) containing a reference to each
        of the parts in this package.
        """
        return tuple([p for p in self._walk_parts(self._rels)])

    @property
    def rels(self):
        """
        Return a reference to the |RelationshipCollection| holding the
        relationships for this package.
        """
        return self._rels

    def save(self, pkg_file):
        """
        Save this package to *pkg_file*, where *file* can be either a path to
        a file (a string) or a file-like object.
        """
        for part in self.parts:
            part._before_marshal()
        PackageWriter.write(pkg_file, self._rels, self.parts)

    def _add_relationship(self, reltype, target, rId, external=False):
        """
        Return newly added |_Relationship| instance of *reltype* between this
        package and part *target* with key *rId*. Target mode is set to
        ``RTM.EXTERNAL`` if *external* is |True|.
        """
        return self._rels.add_relationship(reltype, target, rId, external)

    @staticmethod
    def _walk_parts(rels, visited_parts=None):
        """
        Generate exactly one reference to each of the parts in the package by
        performing a depth-first traversal of the rels graph.
        """
        if visited_parts is None:
            visited_parts = []
        for rel in rels:
            if rel.is_external:
                continue
            part = rel.target_part
            if part in visited_parts:
                continue
            visited_parts.append(part)
            yield part
            for part in OpcPackage._walk_parts(part._rels, visited_parts):
                yield part


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
        self._rels = RelationshipCollection(partname.baseURI)

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

    @property
    def rels(self):
        """
        |RelationshipCollection| instance containing rels for this part.
        """
        return self._rels

    def _add_relationship(self, reltype, target, rId, external=False):
        """
        Return newly added |_Relationship| instance of *reltype* between this
        part and *target* with key *rId*. Target mode is set to
        ``RTM.EXTERNAL`` if *external* is |True|.
        """
        return self._rels.add_relationship(reltype, target, rId, external)

    def _after_unmarshal(self):
        """
        Entry point for post-unmarshaling processing, for example to parse
        the part XML. May be overridden by subclasses without forwarding call
        to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    def _before_marshal(self):
        """
        Entry point for pre-serialization processing, for example to finalize
        part naming if necessary. May be overridden by subclasses without
        forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass


class PartFactory(object):
    """
    Provides a way for client code to specify a subclass of |Part| to be
    constructed by |Unmarshaller| based on its content type.
    """
    part_type_for = {}

    def __new__(cls, partname, content_type, blob):
        if content_type in PartFactory.part_type_for:
            CustomPartClass = PartFactory.part_type_for[content_type]
            return CustomPartClass(partname, content_type, blob)
        return Part(partname, content_type, blob)


class _Relationship(object):
    """
    Value object for relationship to part.
    """
    def __init__(self, rId, reltype, target, baseURI, external=False):
        super(_Relationship, self).__init__()
        self._rId = rId
        self._reltype = reltype
        self._target = target
        self._baseURI = baseURI
        self._is_external = bool(external)

    @property
    def is_external(self):
        return self._is_external

    @property
    def reltype(self):
        return self._reltype

    @property
    def rId(self):
        return self._rId

    @property
    def target_part(self):
        if self._is_external:
            raise ValueError("target_part property on _Relationship is undef"
                             "ined when target mode is External")
        return self._target

    @property
    def target_ref(self):
        if self._is_external:
            return self._target
        else:
            return self._target.partname.relative_ref(self._baseURI)


class RelationshipCollection(object):
    """
    Collection object for |_Relationship| instances, having list semantics.
    """
    def __init__(self, baseURI):
        super(RelationshipCollection, self).__init__()
        self._baseURI = baseURI
        self._rels = []

    def __getitem__(self, key):
        """
        Implements access by subscript, e.g. ``rels[9]``. It also implements
        dict-style lookup of a relationship by rId, e.g. ``rels['rId1']``.
        """
        if isinstance(key, basestring):
            for rel in self._rels:
                if rel.rId == key:
                    return rel
            raise KeyError("no rId '%s' in RelationshipCollection" % key)
        else:
            return self._rels.__getitem__(key)

    def __len__(self):
        """Implements len() built-in on this object"""
        return self._rels.__len__()

    def add_relationship(self, reltype, target, rId, external=False):
        """
        Return a newly added |_Relationship| instance.
        """
        rel = _Relationship(rId, reltype, target, self._baseURI, external)
        self._rels.append(rel)
        return rel

    def get_rel_of_type(self, reltype):
        """
        Return single relationship of type *reltype* from the collection.
        Raises |KeyError| if no matching relationship is found. Raises
        |ValueError| if more than one matching relationship is found.
        """
        matching = [rel for rel in self._rels if rel.reltype == reltype]
        if len(matching) == 0:
            tmpl = "no relationship of type '%s' in collection"
            raise KeyError(tmpl % reltype)
        if len(matching) > 1:
            tmpl = "multiple relationships of type '%s' in collection"
            raise ValueError(tmpl % reltype)
        return matching[0]

    @property
    def xml(self):
        """
        Serialize this relationship collection into XML suitable for storage
        as a .rels file in an OPC package.
        """
        rels_elm = CT_Relationships.new()
        for rel in self._rels:
            rels_elm.add_rel(rel.rId, rel.reltype, rel.target_ref,
                             rel.is_external)
        return rels_elm.xml


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
