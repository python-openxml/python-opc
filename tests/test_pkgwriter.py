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

from opc.pkgwriter import PackageWriter


class DescribePackageWriter(object):

    @pytest.fixture
    def PhysPkgWriter_(self, request):
        _patch = patch('opc.pkgwriter.PhysPkgWriter')
        request.addfinalizer(_patch.stop)
        return _patch.start()

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
