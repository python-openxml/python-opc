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
