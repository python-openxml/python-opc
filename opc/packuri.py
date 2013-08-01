# -*- coding: utf-8 -*-
#
# packuri.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides the PackURI value type along with some useful known values such as
PACKAGE_URI.
"""

import posixpath


class PackURI(str):
    """
    Provides access to pack URI components such as the baseURI and the
    filename slice. Behaves as |str| otherwise.
    """
    def __new__(cls, pack_uri_str):
        if not pack_uri_str[0] == '/':
            tmpl = "PackURI must begin with slash, got '%s'"
            raise ValueError(tmpl % pack_uri_str)
        return str.__new__(cls, pack_uri_str)

    @staticmethod
    def from_rel_ref(baseURI, relative_ref):
        """
        Return a |PackURI| instance containing the absolute pack URI formed by
        translating *relative_ref* onto *baseURI*.
        """
        joined_uri = posixpath.join(baseURI, relative_ref)
        abs_uri = posixpath.abspath(joined_uri)
        return PackURI(abs_uri)

    @property
    def baseURI(self):
        """
        The base URI of this pack URI, the directory portion, roughly
        speaking. E.g. ``'/ppt/slides'`` for ``'/ppt/slides/slide1.xml'``.
        For the package pseudo-partname '/', baseURI is '/'.
        """
        return posixpath.split(self)[0]

    @property
    def ext(self):
        """
        The extension portion of this pack URI, e.g. ``'.xml'`` for
        ``'/ppt/slides/slide1.xml'``. Note that the period is included,
        consistent with the behavior of :meth:`posixpath.ext`.
        """
        return posixpath.splitext(self)[1]

    @property
    def filename(self):
        """
        The "filename" portion of this pack URI, e.g. ``'slide1.xml'`` for
        ``'/ppt/slides/slide1.xml'``. For the package pseudo-partname '/',
        filename is ''.
        """
        return posixpath.split(self)[1]

    @property
    def membername(self):
        """
        The pack URI with the leading slash stripped off, the form used as
        the Zip file membername for the package item. Returns '' for the
        package pseudo-partname '/'.
        """
        return self[1:]

    @property
    def rels_uri(self):
        """
        The pack URI of the .rels part corresponding to the current pack URI.
        Only produces sensible output if the pack URI is a partname or the
        package pseudo-partname '/'.
        """
        rels_filename = '%s.rels' % self.filename
        rels_uri_str = posixpath.join(self.baseURI, '_rels', rels_filename)
        return PackURI(rels_uri_str)


PACKAGE_URI = PackURI('/')
CONTENT_TYPES_URI = PackURI('/[Content_Types].xml')
