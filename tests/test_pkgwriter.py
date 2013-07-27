# -*- coding: utf-8 -*-
#
# test_pkgwriter.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.pkgwriter module."""

import pytest

from mock import call, Mock, patch

from opc.constants import CONTENT_TYPE as CT
from opc.packuri import PackURI
from opc.pkgwriter import _ContentTypesItem, PackageWriter

from .unitutil import function_mock, method_mock


class DescribePackageWriter(object):

    @pytest.fixture
    def PhysPkgWriter_(self, request):
        _patch = patch('opc.pkgwriter.PhysPkgWriter')
        request.addfinalizer(_patch.stop)
        return _patch.start()

    @pytest.fixture
    def xml_for(self, request):
        return method_mock(_ContentTypesItem, 'xml_for', request)

    @pytest.fixture
    def _write_methods(self, request):
        """Mock that patches all the _write_* methods of PackageWriter"""
        root_mock = Mock(name='PackageWriter')
        patch1 = patch.object(PackageWriter, '_write_content_types_stream')
        patch2 = patch.object(PackageWriter, '_write_pkg_rels')
        patch3 = patch.object(PackageWriter, '_write_parts')
        root_mock.attach_mock(patch1.start(), '_write_content_types_stream')
        root_mock.attach_mock(patch2.start(), '_write_pkg_rels')
        root_mock.attach_mock(patch3.start(), '_write_parts')

        def fin():
            patch1.stop()
            patch2.stop()
            patch3.stop()

        request.addfinalizer(fin)
        return root_mock

    def it_can_write_a_package(self, PhysPkgWriter_, _write_methods):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        pkg_rels = Mock(name='pkg_rels')
        parts = Mock(name='parts')
        phys_writer = PhysPkgWriter_.return_value
        # exercise ---------------------
        PackageWriter.write(pkg_file, pkg_rels, parts)
        # verify -----------------------
        expected_calls = [
            call._write_content_types_stream(phys_writer, parts),
            call._write_pkg_rels(phys_writer, pkg_rels),
            call._write_parts(phys_writer, parts),
        ]
        PhysPkgWriter_.assert_called_once_with(pkg_file)
        assert _write_methods.mock_calls == expected_calls
        phys_writer.close.assert_called_once_with()

    def it_can_write_a_content_types_stream(self, xml_for):
        # mockery ----------------------
        phys_writer = Mock(name='phys_writer')
        parts = Mock(name='parts')
        # exercise ---------------------
        PackageWriter._write_content_types_stream(phys_writer, parts)
        # verify -----------------------
        xml_for.assert_called_once_with(parts)
        phys_writer.write.assert_called_once_with('/[Content_Types].xml',
                                                  xml_for.return_value)

    def it_can_write_a_pkg_rels_item(self):
        # mockery ----------------------
        phys_writer = Mock(name='phys_writer')
        pkg_rels = Mock(name='pkg_rels')
        # exercise ---------------------
        PackageWriter._write_pkg_rels(phys_writer, pkg_rels)
        # verify -----------------------
        phys_writer.write.assert_called_once_with('/_rels/.rels',
                                                  pkg_rels.xml)


class Describe_ContentTypesItem(object):

    @pytest.fixture
    def oxml_tostring(self, request):
        return function_mock('opc.pkgwriter.oxml_tostring', request)

    @pytest.fixture
    def parts(self):
        """list of parts that will exercise _ContentTypesItem.xml_for()"""
        return [
            Mock(name='part_1', partname=PackURI('/docProps/core.xml'),
                 content_type='app/vnd.core'),
            Mock(name='part_2', partname=PackURI('/docProps/thumbnail.jpeg'),
                 content_type=CT.JPEG),
            Mock(name='part_3', partname=PackURI('/ppt/slides/slide2.xml'),
                 content_type='app/vnd.ct_sld'),
            Mock(name='part_4', partname=PackURI('/ppt/slides/slide1.xml'),
                 content_type='app/vnd.ct_sld'),
            Mock(name='part_5', partname=PackURI('/zebra/foo.bar'),
                 content_type='app/vnd.foobar'),
        ]

    @pytest.fixture
    def types(self, request):
        """Mock returned by CT_Types.new() call"""
        types = Mock(name='types')
        _patch = patch('opc.pkgwriter.CT_Types')
        CT_Types = _patch.start()
        CT_Types.new.return_value = types
        request.addfinalizer(_patch.stop)
        return types

    def it_can_compose_content_types_xml(self, parts, types, oxml_tostring):
        # # exercise ---------------------
        _ContentTypesItem.xml_for(parts)
        # verify -----------------------
        expected_types_calls = [
            call.add_default('.jpeg', CT.JPEG),
            call.add_default('.rels', CT.OPC_RELATIONSHIPS),
            call.add_default('.xml',  CT.XML),
            call.add_override('/docProps/core.xml',     'app/vnd.core'),
            call.add_override('/ppt/slides/slide1.xml', 'app/vnd.ct_sld'),
            call.add_override('/ppt/slides/slide2.xml', 'app/vnd.ct_sld'),
            call.add_override('/zebra/foo.bar',         'app/vnd.foobar'),
        ]
        assert types.mock_calls == expected_types_calls
        oxml_tostring.assert_called_once_with(types, encoding='UTF-8',
                                              standalone=True),
