# -*- coding: utf-8 -*-
#
# opc_steps.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Acceptance test steps for python-opc."""

import hashlib
import os

from behave import given, when, then

from opc import OpcPackage
from opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT


def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))

thisdir = os.path.split(__file__)[0]
test_file_dir = absjoin(thisdir, '../../tests/test_files')
basic_pptx_path = absjoin(test_file_dir, 'test.pptx')


# given ====================================================

@given('a python-opc working environment')
def step_given_python_opc_working_environment(context):
    pass


# when =====================================================

@when('I open a PowerPoint file')
def step_when_open_basic_pptx(context):
    context.pkg = OpcPackage.open(basic_pptx_path)


# then =====================================================

@then('the expected package rels are loaded')
def step_then_expected_pkg_rels_loaded(context):
    expected_rel_values = (
        ('rId1', RT.OFFICE_DOCUMENT,     False, '/ppt/presentation.xml'),
        ('rId2', RT.THUMBNAIL,           False, '/docProps/thumbnail.jpeg'),
        ('rId3', RT.CORE_PROPERTIES,     False, '/docProps/core.xml'),
        ('rId4', RT.EXTENDED_PROPERTIES, False, '/docProps/app.xml'),
    )
    assert len(expected_rel_values) == len(context.pkg.rels)
    for rId, reltype, is_external, partname in expected_rel_values:
        rel = context.pkg.rels[rId]
        assert rel.rId == rId, "rId is '%s'" % rel.rId
        assert rel.reltype == reltype, "reltype is '%s'" % rel.reltype
        assert rel.is_external == is_external
        assert rel.target_part.partname == partname, (
            "target partname is '%s'" % rel.target_part.partname)


@then('the expected parts are loaded')
def step_then_expected_parts_are_loaded(context):
    expected_part_values = {
        '/docProps/app.xml': (
            CT.OFC_EXTENDED_PROPERTIES, 'e5a7552c35180b9796f2132d39bc0d208cf'
            '8761f', []
        ),
        '/docProps/core.xml': (
            CT.OPC_CORE_PROPERTIES, '08c8ff0912231db740fa1277d8fa4ef175a306e'
            '4', []
        ),
        '/docProps/thumbnail.jpeg': (
            CT.JPEG, '8a93420017d57f9c69f802639ee9791579b21af5', []
        ),
        '/ppt/presentation.xml': (
            CT.PML_PRESENTATION_MAIN,
            'efa7bee0ac72464903a67a6744c1169035d52a54',
            [
                ('rId1', RT.SLIDE_MASTER, False,
                 '/ppt/slideMasters/slideMaster1.xml'),
                ('rId2', RT.SLIDE, False, '/ppt/slides/slide1.xml'),
                ('rId3', RT.PRINTER_SETTINGS, False,
                 '/ppt/printerSettings/printerSettings1.bin'),
                ('rId4', RT.PRES_PROPS, False, '/ppt/presProps.xml'),
                ('rId5', RT.VIEW_PROPS, False, '/ppt/viewProps.xml'),
                ('rId6', RT.THEME, False, '/ppt/theme/theme1.xml'),
                ('rId7', RT.TABLE_STYLES, False, '/ppt/tableStyles.xml'),
            ]
        ),
        '/ppt/printerSettings/printerSettings1.bin': (
            CT.PML_PRINTER_SETTINGS, 'b0feb4cc107c9b2d135b1940560cf8f045ffb7'
            '46', []
        ),
        '/ppt/presProps.xml': (
            CT.PML_PRES_PROPS, '7d4981fd742429e6b8cc99089575ac0ee7db5194', []
        ),
        '/ppt/viewProps.xml': (
            CT.PML_VIEW_PROPS, '172a42a6be09d04eab61ae3d49eff5580a4be451', []
        ),
        '/ppt/theme/theme1.xml': (
            CT.OFC_THEME, '9f362326d8dc050ab6eef7f17335094bd06da47e', []
        ),
        '/ppt/tableStyles.xml': (
            CT.PML_TABLE_STYLES, '49bfd13ed02199b004bf0a019a596f127758d926',
            []
        ),
        '/ppt/slideMasters/slideMaster1.xml': (
            CT.PML_SLIDE_MASTER, 'be6fe53e199ef10259227a447e4ac9530803ecce',
            [
                ('rId1', RT.SLIDE_LAYOUT, False,
                 '/ppt/slideLayouts/slideLayout1.xml'),
                ('rId2', RT.SLIDE_LAYOUT, False,
                 '/ppt/slideLayouts/slideLayout2.xml'),
                ('rId3', RT.SLIDE_LAYOUT, False,
                 '/ppt/slideLayouts/slideLayout3.xml'),
                ('rId4', RT.THEME, False, '/ppt/theme/theme1.xml'),
            ],
        ),
        '/ppt/slideLayouts/slideLayout1.xml': (
            CT.PML_SLIDE_LAYOUT, 'bcbeb908e22346fecda6be389759ca9ed068693c',
            [
                ('rId1', RT.SLIDE_MASTER, False,
                 '/ppt/slideMasters/slideMaster1.xml'),
            ],
        ),
        '/ppt/slideLayouts/slideLayout2.xml': (
            CT.PML_SLIDE_LAYOUT, '316d0fb0ce4c3560fa2ed4edc3becf2c4ce84b6b',
            [
                ('rId1', RT.SLIDE_MASTER, False,
                 '/ppt/slideMasters/slideMaster1.xml'),
            ],
        ),
        '/ppt/slideLayouts/slideLayout3.xml': (
            CT.PML_SLIDE_LAYOUT, '5b704e54c995b7d1bd7d24ef996a573676cc15ca',
            [
                ('rId1', RT.SLIDE_MASTER, False,
                 '/ppt/slideMasters/slideMaster1.xml'),
            ],
        ),
        '/ppt/slides/slide1.xml': (
            CT.PML_SLIDE, '1841b18f1191629c70b7176d8e210fa2ef079d85',
            [
                ('rId1', RT.SLIDE_LAYOUT, False,
                 '/ppt/slideLayouts/slideLayout1.xml'),
                ('rId2', RT.HYPERLINK, True,
                 'https://github.com/scanny/python-pptx'),
            ]
        ),
    }
    assert len(context.pkg.parts) == len(expected_part_values), (
        "len(context.pkg.parts) is %d" % len(context.pkg.parts))
    for part in context.pkg.parts:
        partname = part.partname
        content_type, sha1, exp_rel_vals = expected_part_values[partname]
        assert part.content_type == content_type, (
            "content_type for %s is '%s'" % (partname, part.content_type))
        blob_sha1 = hashlib.sha1(part.blob).hexdigest()
        assert blob_sha1 == sha1, ("SHA1 for %s is '%s'" %
                                   (partname, blob_sha1))
        assert len(part.rels) == len(exp_rel_vals), (
            "len(part.rels) for %s is %d" % (partname, len(part.rels)))
        for rId, reltype, is_external, target in exp_rel_vals:
            rel = part.rels[rId]
            assert rel.rId == rId, "rId is '%s'" % rel.rId
            assert rel.reltype == reltype, ("reltype for %s on %s is '%s'" %
                                            (rId, partname, rel.reltype))
            assert rel.is_external == is_external
            if rel.is_external:
                assert rel.target_ref == target, (
                    "target_ref for %s on %s is '%s'" %
                    (rId, partname, rel.target_ref))
            else:
                assert rel.target_part.partname == target, (
                    "target partname for %s on %s is '%s'" %
                    (rId, partname, rel.target_part.partname))
