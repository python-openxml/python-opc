# -*- coding: utf-8 -*-
#
# test_package.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.package module."""

import pytest

from mock import Mock

from opc.package import OpcPackage

from .unitutil import class_mock


class DescribeOpcPackage(object):

    @pytest.fixture
    def PackageReader_(self, request):
        return class_mock('opc.package.PackageReader', request)

    @pytest.fixture
    def PartFactory_(self, request):
        return class_mock('opc.package.PartFactory', request)

    @pytest.fixture
    def Unmarshaller_(self, request):
        return class_mock('opc.package.Unmarshaller', request)

    def it_can_open_a_pkg_file(self, PackageReader_, PartFactory_,
                               Unmarshaller_):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        pkg_reader = PackageReader_.from_file.return_value
        # exercise ---------------------
        pkg = OpcPackage.open(pkg_file)
        # verify -----------------------
        PackageReader_.from_file.assert_called_once_with(pkg_file)
        Unmarshaller_.unmarshal.assert_called_once_with(pkg_reader, pkg,
                                                        PartFactory_)
        assert isinstance(pkg, OpcPackage)
