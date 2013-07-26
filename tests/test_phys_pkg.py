# -*- coding: utf-8 -*-
#
# test_phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.phys_pkg module."""

try:
    from io import BytesIO  # Python 3
except ImportError:
    from StringIO import StringIO as BytesIO

import hashlib

from zipfile import ZIP_DEFLATED, ZipFile

from opc.packuri import PACKAGE_URI, PackURI
from opc.phys_pkg import (
    PhysPkgReader, PhysPkgWriter, ZipPkgReader, ZipPkgWriter
)

import pytest

from mock import Mock

from .unitutil import abspath, class_mock


test_pptx_path = abspath('test_files/test.pptx')


@pytest.fixture
def ZipFile_(request):
    return class_mock('opc.phys_pkg.ZipFile', request)


class DescribePhysPkgReader(object):

    @pytest.fixture
    def ZipPkgReader_(self, request):
        return class_mock('opc.phys_pkg.ZipPkgReader', request)

    def it_constructs_a_pkg_reader_instance(self, ZipPkgReader_):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        # exercise ---------------------
        phys_pkg_reader = PhysPkgReader(pkg_file)
        # verify -----------------------
        ZipPkgReader_.assert_called_once_with(pkg_file)
        assert phys_pkg_reader == ZipPkgReader_.return_value


class DescribePhysPkgWriter(object):

    @pytest.fixture
    def ZipPkgWriter_(self, request):
        return class_mock('opc.phys_pkg.ZipPkgWriter', request)

    def it_constructs_a_pkg_writer_instance(self, ZipPkgWriter_):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        # exercise ---------------------
        phys_pkg_writer = PhysPkgWriter(pkg_file)
        # verify -----------------------
        ZipPkgWriter_.assert_called_once_with(pkg_file)
        assert phys_pkg_writer == ZipPkgWriter_.return_value


class DescribeZipPkgReader(object):

    @pytest.fixture(scope='class')
    def phys_reader(self, request):
        phys_reader = ZipPkgReader(test_pptx_path)
        request.addfinalizer(phys_reader.close)
        return phys_reader

    def it_opens_pkg_file_zip_on_construction(self, ZipFile_):
        pkg_file = Mock(name='pkg_file')
        ZipPkgReader(pkg_file)
        ZipFile_.assert_called_once_with(pkg_file, 'r')

    def it_can_be_closed(self, ZipFile_):
        # mockery ----------------------
        zipf = ZipFile_.return_value
        zip_pkg_reader = ZipPkgReader(None)
        # exercise ---------------------
        zip_pkg_reader.close()
        # verify -----------------------
        zipf.close.assert_called_once_with()

    def it_can_retrieve_the_blob_for_a_pack_uri(self, phys_reader):
        pack_uri = PackURI('/ppt/presentation.xml')
        blob = phys_reader.blob_for(pack_uri)
        sha1 = hashlib.sha1(blob).hexdigest()
        assert sha1 == 'efa7bee0ac72464903a67a6744c1169035d52a54'

    def it_has_the_content_types_xml(self, phys_reader):
        sha1 = hashlib.sha1(phys_reader.content_types_xml).hexdigest()
        assert sha1 == '9604a4fb3bf9626f5ad59a4e82029b3a501f106a'

    def it_can_retrieve_rels_xml_for_source_uri(self, phys_reader):
        rels_xml = phys_reader.rels_xml_for(PACKAGE_URI)
        sha1 = hashlib.sha1(rels_xml).hexdigest()
        assert sha1 == 'e31451d4bbe7d24adbe21454b8e9fdae92f50de5'

    def it_returns_none_when_part_has_no_rels_xml(self, phys_reader):
        partname = PackURI('/ppt/viewProps.xml')
        rels_xml = phys_reader.rels_xml_for(partname)
        assert rels_xml is None


class DescribeZipPkgWriter(object):

    @pytest.fixture
    def pkg_file(self, request):
        pkg_file = BytesIO()
        request.addfinalizer(pkg_file.close)
        return pkg_file

    def it_opens_pkg_file_zip_on_construction(self, ZipFile_):
        pkg_file = Mock(name='pkg_file')
        ZipPkgWriter(pkg_file)
        ZipFile_.assert_called_once_with(pkg_file, 'w',
                                         compression=ZIP_DEFLATED)

    def it_can_be_closed(self, ZipFile_):
        # mockery ----------------------
        zipf = ZipFile_.return_value
        zip_pkg_writer = ZipPkgWriter(None)
        # exercise ---------------------
        zip_pkg_writer.close()
        # verify -----------------------
        zipf.close.assert_called_once_with()

    def it_can_write_a_blob(self, pkg_file):
        # setup ------------------------
        pack_uri = PackURI('/part/name.xml')
        blob = '<BlobbityFooBlob/>'.encode('utf-8')
        # exercise ---------------------
        pkg_writer = PhysPkgWriter(pkg_file)
        pkg_writer.write(pack_uri, blob)
        pkg_writer.close()
        # verify -----------------------
        written_blob_sha1 = hashlib.sha1(blob).hexdigest()
        zipf = ZipFile(pkg_file, 'r')
        retrieved_blob = zipf.read(pack_uri.membername)
        zipf.close()
        retrieved_blob_sha1 = hashlib.sha1(retrieved_blob).hexdigest()
        assert retrieved_blob_sha1 == written_blob_sha1
