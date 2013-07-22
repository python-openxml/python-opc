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

from mock import call, Mock

from opc.package import (
    OpcPackage, Part, PartFactory, RelationshipCollection, Unmarshaller
)
from opc.packuri import PACKAGE_URI

from .unitutil import class_mock, method_mock


@pytest.fixture
def RelationshipCollection_(request):
    return class_mock('opc.package.RelationshipCollection', request)


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

    def it_initializes_its_rels_collection_on_construction(
            self, RelationshipCollection_):
        pkg = OpcPackage()
        RelationshipCollection_.assert_called_once_with(PACKAGE_URI.baseURI)
        assert pkg.rels == RelationshipCollection_.return_value


class DescribePart(object):

    def it_remembers_its_construction_state(self):
        partname, content_type, blob = (
            Mock(name='partname'), Mock(name='content_type'),
            Mock(name='blob')
        )
        part = Part(partname, content_type, blob)
        assert part.blob == blob
        assert part.content_type == content_type
        assert part.partname == partname

    def it_can_be_notified_after_unmarshalling_is_complete(self):
        part = Part(None, None, None)
        part._after_unmarshal()


class DescribePartFactory(object):

    @pytest.fixture
    def Part_(self, request):
        return class_mock('opc.package.Part', request)

    def it_constructs_a_part_instance(self, Part_):
        # mockery ----------------------
        partname, content_type, blob = (
            Mock(name='partname'), Mock(name='content_type'),
            Mock(name='blob')
        )
        # exercise ---------------------
        part = PartFactory(partname, content_type, blob)
        # verify -----------------------
        Part_.assert_called_once_with(partname, content_type, blob)
        assert part == Part_.return_value


class DescribeRelationshipCollection(object):

    def it_has_a_len(self):
        rels = RelationshipCollection(None)
        assert len(rels) == 0


class DescribeUnmarshaller(object):

    @pytest.fixture
    def _unmarshal_parts(self, request):
        return method_mock(Unmarshaller, '_unmarshal_parts', request)

    @pytest.fixture
    def _unmarshal_relationships(self, request):
        return method_mock(Unmarshaller, '_unmarshal_relationships', request)

    def it_can_unmarshal_from_a_pkg_reader(self, _unmarshal_parts,
                                           _unmarshal_relationships):
        # mockery ----------------------
        pkg = Mock(name='pkg')
        pkg_reader = Mock(name='pkg_reader')
        part_factory = Mock(name='part_factory')
        parts = {1: Mock(name='part_1'), 2: Mock(name='part_2')}
        _unmarshal_parts.return_value = parts
        # exercise ---------------------
        Unmarshaller.unmarshal(pkg_reader, pkg, part_factory)
        # verify -----------------------
        _unmarshal_parts.assert_called_once_with(pkg_reader, part_factory)
        _unmarshal_relationships.assert_called_once_with(pkg_reader, pkg,
                                                         parts)
        for part in parts.values():
            part._after_unmarshal.assert_called_once_with()

    def it_can_unmarshal_parts(self):
        # test data --------------------
        part_properties = (
            ('/part/name1.xml', 'app/vnd.contentType_A', '<Part_1/>'),
            ('/part/name2.xml', 'app/vnd.contentType_B', '<Part_2/>'),
            ('/part/name3.xml', 'app/vnd.contentType_C', '<Part_3/>'),
        )
        # mockery ----------------------
        pkg_reader = Mock(name='pkg_reader')
        pkg_reader.iter_sparts.return_value = part_properties
        part_factory = Mock(name='part_factory')
        parts = [Mock(name='part1'), Mock(name='part2'), Mock(name='part3')]
        part_factory.side_effect = parts
        # exercise ---------------------
        retval = Unmarshaller._unmarshal_parts(pkg_reader, part_factory)
        # verify -----------------------
        expected_calls = [call(*p) for p in part_properties]
        expected_parts = dict((p[0], parts[idx]) for (idx, p) in
                              enumerate(part_properties))
        assert part_factory.call_args_list == expected_calls
        assert retval == expected_parts

    def it_can_unmarshal_relationships(self):
        # test data --------------------
        reltype = 'http://reltype'
        # mockery ----------------------
        pkg_reader = Mock(name='pkg_reader')
        pkg_reader.iter_srels.return_value = (
            ('/',         Mock(name='srel1', rId='rId1', reltype=reltype,
             target_partname='partname1', is_external=False)),
            ('/',         Mock(name='srel2', rId='rId2', reltype=reltype,
             target_ref='target_ref_1',   is_external=True)),
            ('partname1', Mock(name='srel3', rId='rId3', reltype=reltype,
             target_partname='partname2', is_external=False)),
            ('partname2', Mock(name='srel4', rId='rId4', reltype=reltype,
             target_ref='target_ref_2',   is_external=True)),
        )
        pkg = Mock(name='pkg')
        parts = {}
        for num in range(1, 3):
            name = 'part%d' % num
            part = Mock(name=name)
            parts['partname%d' % num] = part
            pkg.attach_mock(part, name)
        # exercise ---------------------
        Unmarshaller._unmarshal_relationships(pkg_reader, pkg, parts)
        # verify -----------------------
        expected_pkg_calls = [
            call._add_relationship(
                reltype, parts['partname1'], 'rId1', False),
            call._add_relationship(
                reltype, 'target_ref_1', 'rId2', True),
            call.part1._add_relationship(
                reltype, parts['partname2'], 'rId3', False),
            call.part2._add_relationship(
                reltype, 'target_ref_2', 'rId4', True),
        ]
        assert pkg.mock_calls == expected_pkg_calls
