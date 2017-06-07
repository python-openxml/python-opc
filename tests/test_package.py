# -*- coding: utf-8 -*-
#
# test_package.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.package module."""

import pytest

from mock import call, Mock, patch, PropertyMock

from opc.constants import CONTENT_TYPE as CT
from opc.oxml import CT_Relationships
from opc.package import (
    OpcPackage, Part, PartFactory, _Relationship, RelationshipCollection,
    Unmarshaller
)
from opc.packuri import PACKAGE_URI, PackURI

from .unitutil import class_mock, method_mock


@pytest.fixture
def RelationshipCollection_(request):
    return class_mock('opc.package.RelationshipCollection', request)


class DescribeOpcPackage(object):

    @pytest.fixture
    def PackageReader_(self, request):
        return class_mock('opc.package.PackageReader', request)

    @pytest.fixture
    def PackageWriter_(self, request):
        return class_mock('opc.package.PackageWriter', request)

    @pytest.fixture
    def PartFactory_(self, request):
        return class_mock('opc.package.PartFactory', request)

    @pytest.fixture
    def parts(self, request):
        """
        Return a mock patching property OpcPackage.parts, reversing the
        patch after each use.
        """
        _patch = patch.object(OpcPackage, 'parts', new_callable=PropertyMock)
        request.addfinalizer(_patch.stop)
        return _patch.start()

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

    def it_can_add_a_relationship_to_a_part(self):
        # mockery ----------------------
        reltype, target, rId = (
            Mock(name='reltype'), Mock(name='target'), Mock(name='rId')
        )
        pkg = OpcPackage()
        pkg._rels = Mock(name='_rels')
        # exercise ---------------------
        pkg._add_relationship(reltype, target, rId)
        # verify -----------------------
        pkg._rels.add_relationship.assert_called_once_with(reltype, target,
                                                           rId, False)

    def it_has_an_immutable_sequence_containing_its_parts(self):
        # mockery ----------------------
        parts = [Mock(name='part1'), Mock(name='part2')]
        pkg = OpcPackage()
        # verify -----------------------
        with patch.object(OpcPackage, '_walk_parts', return_value=parts):
            assert pkg.parts == (parts[0], parts[1])

    def it_can_iterate_over_parts_by_walking_rels_graph(self):
        # +----------+       +--------+
        # | pkg_rels |-----> | part_1 |
        # +----------+       +--------+
        #      |               |    ^
        #      v               v    |
        #   external         +--------+
        #                    | part_2 |
        #                    +--------+
        part1, part2 = (Mock(name='part1'), Mock(name='part2'))
        part1._rels = [Mock(name='rel1', is_external=False, target_part=part2)]
        part2._rels = [Mock(name='rel2', is_external=False, target_part=part1)]
        pkg_rels = [
            Mock(name='rel3', is_external=False, target_part=part1),
            Mock(name='rel3', is_external=True),
        ]
        # exercise ---------------------
        generated_parts = [part for part in OpcPackage._walk_parts(pkg_rels)]
        # verify -----------------------
        assert generated_parts == [part1, part2]

    def it_can_save_to_a_pkg_file(self, PackageWriter_, parts):
        # mockery ----------------------
        pkg_file = Mock(name='pkg_file')
        pkg = OpcPackage()
        parts.return_value = parts = [Mock(name='part1'), Mock(name='part2')]
        # exercise ---------------------
        pkg.save(pkg_file)
        # verify -----------------------
        for part in parts:
            part._before_marshal.assert_called_once_with()
        PackageWriter_.write.assert_called_once_with(pkg_file, pkg._rels,
                                                     parts)


class DescribePart(object):

    @pytest.fixture
    def part(self):
        partname = Mock(name='partname', baseURI='/')
        return Part(partname, None, None)

    def it_remembers_its_construction_state(self):
        partname, content_type, blob = (
            Mock(name='partname'), Mock(name='content_type'),
            Mock(name='blob')
        )
        part = Part(partname, content_type, blob)
        assert part.blob == blob
        assert part.content_type == content_type
        assert part.partname == partname

    def it_has_a_rels_collection_it_initializes_on_construction(
            self, RelationshipCollection_):
        partname = Mock(name='partname', baseURI='/')
        part = Part(partname, None, None)
        RelationshipCollection_.assert_called_once_with('/')
        assert part.rels == RelationshipCollection_.return_value

    def it_can_add_a_relationship_to_another_part(self, part):
        # mockery ----------------------
        reltype, target, rId = (
            Mock(name='reltype'), Mock(name='target'), Mock(name='rId')
        )
        part._rels = Mock(name='_rels')
        # exercise ---------------------
        part._add_relationship(reltype, target, rId)
        # verify -----------------------
        part._rels.add_relationship.assert_called_once_with(reltype, target,
                                                            rId, False)

    def it_can_be_notified_after_unmarshalling_is_complete(self, part):
        part._after_unmarshal()

    def it_can_be_notified_before_marshalling_is_started(self, part):
        part._before_marshal()


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

    def it_constructs_custom_part_type_for_registered_content_types(self):
        # mockery ----------------------
        CustomPartClass = Mock(name='CustomPartClass')
        partname, blob = (Mock(name='partname'), Mock(name='blob'))
        # exercise ---------------------
        PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = CustomPartClass
        part = PartFactory(partname, CT.WML_DOCUMENT_MAIN, blob)
        # verify -----------------------
        CustomPartClass.load.assert_called_once_with(partname,
                                                CT.WML_DOCUMENT_MAIN, blob)
        assert part is CustomPartClass.load.return_value


class Describe_Relationship(object):

    def it_remembers_construction_values(self):
        # test data --------------------
        rId = 'rId9'
        reltype = 'reltype'
        target = Mock(name='target_part')
        external = False
        # exercise ---------------------
        rel = _Relationship(rId, reltype, target, None, external)
        # verify -----------------------
        assert rel.rId == rId
        assert rel.reltype == reltype
        assert rel.target_part == target
        assert rel.is_external == external

    def it_should_raise_on_target_part_access_on_external_rel(self):
        rel = _Relationship(None, None, None, None, external=True)
        with pytest.raises(ValueError):
            rel.target_part

    def it_should_have_target_ref_for_external_rel(self):
        rel = _Relationship(None, None, 'target', None, external=True)
        assert rel.target_ref == 'target'

    def it_should_have_relative_ref_for_internal_rel(self):
        """
        Internal relationships (TargetMode == 'Internal' in the XML) should
        have a relative ref, e.g. '../slideLayouts/slideLayout1.xml', for
        the target_ref attribute.
        """
        part = Mock(name='part', partname=PackURI('/ppt/media/image1.png'))
        baseURI = '/ppt/slides'
        rel = _Relationship(None, None, part, baseURI)  # external=False
        assert rel.target_ref == '../media/image1.png'


class DescribeRelationshipCollection(object):

    @pytest.fixture
    def _Relationship_(self, request):
        return class_mock('opc.package._Relationship', request)

    @pytest.fixture
    def rels(self):
        """
        Populated RelationshipCollection instance that will exercise the
        rels.xml property.
        """
        rels = RelationshipCollection('/baseURI')
        rels.add_relationship(
            reltype='http://rt-hyperlink', target='http://some/link',
            rId='rId1', external=True
        )
        part = Mock(name='part')
        part.partname.relative_ref.return_value = '../media/image1.png'
        rels.add_relationship(reltype='http://rt-image', target=part,
                              rId='rId2')
        return rels

    @pytest.fixture
    def rels_elm(self, request):
        """
        Return a rels_elm mock that will be returned from
        CT_Relationships.new()
        """
        # create rels_elm mock with a .xml property
        rels_elm = Mock(name='rels_elm')
        xml = PropertyMock(name='xml')
        type(rels_elm).xml = xml
        rels_elm.attach_mock(xml, 'xml')
        rels_elm.reset_mock()  # to clear attach_mock call
        # patch CT_Relationships to return that rels_elm
        patch_ = patch.object(CT_Relationships, 'new', return_value=rels_elm)
        patch_.start()
        request.addfinalizer(patch_.stop)
        return rels_elm

    def it_has_a_len(self):
        rels = RelationshipCollection(None)
        assert len(rels) == 0

    def it_supports_indexed_access(self):
        rels = RelationshipCollection(None)
        try:
            rels[0]
        except TypeError:
            msg = 'RelationshipCollection does not support indexed access'
            pytest.fail(msg)
        except IndexError:
            pass

    def it_has_dict_style_lookup_of_rel_by_rId(self):
        rel = Mock(name='rel', rId='foobar')
        rels = RelationshipCollection(None)
        rels._rels.append(rel)
        assert rels['foobar'] == rel

    def it_should_raise_on_failed_lookup_by_rId(self):
        rel = Mock(name='rel', rId='foobar')
        rels = RelationshipCollection(None)
        rels._rels.append(rel)
        with pytest.raises(KeyError):
            rels['barfoo']

    def it_can_add_a_relationship(self, _Relationship_):
        baseURI, rId, reltype, target, external = (
            'baseURI', 'rId9', 'reltype', 'target', False
        )
        rels = RelationshipCollection(baseURI)
        rel = rels.add_relationship(reltype, target, rId, external)
        _Relationship_.assert_called_once_with(rId, reltype, target, baseURI,
                                               external)
        assert rels[0] == rel
        assert rel == _Relationship_.return_value

    def it_can_compose_rels_xml(self, rels, rels_elm):
        # exercise ---------------------
        rels.xml
        # trace ------------------------
        print('Actual calls:\n%s' % rels_elm.mock_calls)
        # verify -----------------------
        expected_rels_elm_calls = [
            call.add_rel('rId1', 'http://rt-hyperlink', 'http://some/link',
                         True),
            call.add_rel('rId2', 'http://rt-image', '../media/image1.png',
                         False),
            call.xml()
        ]
        assert rels_elm.mock_calls == expected_rels_elm_calls


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
