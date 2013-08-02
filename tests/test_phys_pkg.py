# -*- coding: utf-8 -*-
#
# test_phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.phys_pkg module."""

from opc.phys_pkg import PhysPkgReader, ZipPkgReader

import pytest

from mock import Mock

from .unitutil import class_mock


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


class DescribeZipPkgReader(object):

    def it_opens_pkg_file_zip_on_construction(self, ZipFile_):
        pkg_file = Mock(name='pkg_file')
        ZipPkgReader(pkg_file)
        ZipFile_.assert_called_once_with(pkg_file, 'r')
