# -*- coding: utf-8 -*-
#
# test_pkgreader.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.pkgreader module."""

import pytest

from mock import call, Mock, patch

from opc.phys_pkg import ZipPkgReader
from opc.pkgreader import _ContentTypeMap, PackageReader

from .unitutil import class_mock, initializer_mock, method_mock


class DescribePackageReader(object):

    @pytest.fixture
    def from_xml(self, request):
        return method_mock(_ContentTypeMap, 'from_xml', request)

    @pytest.fixture
    def init(self, request):
        return initializer_mock(PackageReader, request)

    @pytest.fixture
    def _load_serialized_parts(self, request):
        return method_mock(PackageReader, '_load_serialized_parts', request)

    @pytest.fixture
    def PhysPkgReader_(self, request):
        _patch = patch('opc.pkgreader.PhysPkgReader', spec_set=ZipPkgReader)
        request.addfinalizer(_patch.stop)
        return _patch.start()

    @pytest.fixture
    def _SerializedPart_(self, request):
        return class_mock('opc.pkgreader._SerializedPart', request)

    @pytest.fixture
    def _srels_for(self, request):
        return method_mock(PackageReader, '_srels_for', request)

    @pytest.fixture
    def _walk_phys_parts(self, request):
        return method_mock(PackageReader, '_walk_phys_parts', request)

    def it_can_construct_from_pkg_file(self, init, PhysPkgReader_, from_xml,
                                       _srels_for, _load_serialized_parts):
        # mockery ----------------------
        phys_reader = PhysPkgReader_.return_value
        content_types = from_xml.return_value
        pkg_srels = _srels_for.return_value
        sparts = _load_serialized_parts.return_value
        pkg_file = Mock(name='pkg_file')
        # exercise ---------------------
        pkg_reader = PackageReader.from_file(pkg_file)
        # verify -----------------------
        PhysPkgReader_.assert_called_once_with(pkg_file)
        from_xml.assert_called_once_with(phys_reader.content_types_xml)
        _srels_for.assert_called_once_with(phys_reader, '/')
        _load_serialized_parts.assert_called_once_with(phys_reader, pkg_srels,
                                                       content_types)
        phys_reader.close.assert_called_once_with()
        init.assert_called_once_with(content_types, pkg_srels, sparts)
        assert isinstance(pkg_reader, PackageReader)

    def it_can_iterate_over_the_serialized_parts(self):
        # mockery ----------------------
        partname, content_type, blob = ('part/name.xml', 'app/vnd.type',
                                        '<Part_1/>')
        spart = Mock(name='spart', partname=partname,
                     content_type=content_type, blob=blob)
        pkg_reader = PackageReader(None, None, [spart])
        iter_count = 0
        # exercise ---------------------
        for retval in pkg_reader.iter_sparts():
            iter_count += 1
        # verify -----------------------
        assert retval == (partname, content_type, blob)
        assert iter_count == 1

    def it_can_load_serialized_parts(self, _SerializedPart_, _walk_phys_parts):
        # test data --------------------
        test_data = (
            ('/part/name1.xml', 'app/vnd.type_1', '<Part_1/>', 'srels_1'),
            ('/part/name2.xml', 'app/vnd.type_2', '<Part_2/>', 'srels_2'),
        )
        iter_vals = [(t[0], t[2], t[3]) for t in test_data]
        content_types = dict((t[0], t[1]) for t in test_data)
        # mockery ----------------------
        phys_reader = Mock(name='phys_reader')
        pkg_srels = Mock(name='pkg_srels')
        _walk_phys_parts.return_value = iter_vals
        _SerializedPart_.side_effect = expected_sparts = (
            Mock(name='spart_1'), Mock(name='spart_2')
        )
        # exercise ---------------------
        retval = PackageReader._load_serialized_parts(phys_reader, pkg_srels,
                                                      content_types)
        # verify -----------------------
        expected_calls = [
            call('/part/name1.xml', 'app/vnd.type_1', '<Part_1/>', 'srels_1'),
            call('/part/name2.xml', 'app/vnd.type_2', '<Part_2/>', 'srels_2'),
        ]
        assert _SerializedPart_.call_args_list == expected_calls
        assert retval == expected_sparts
