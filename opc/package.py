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

from opc.pkgreader import PackageReader


class OpcPackage(object):
    """
    Main API class for |python-opc|. A new instance is constructed by calling
    the :meth:`open` class method with a path to a package file or file-like
    object containing one.
    """
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


class PartFactory(object):
    """
    Provides a way for client code to specify a subclass of |Part| to be
    constructed by |Unmarshaller| based on its content type.
    """


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
