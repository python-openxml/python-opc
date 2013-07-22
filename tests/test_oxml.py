# -*- coding: utf-8 -*-
#
# test_oxml.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-pptx and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for opc.oxml module."""

from opc.constants import RELATIONSHIP_TARGET_MODE as RTM

from .unitdata import a_Default, an_Override, a_Relationship


class DescribeCT_Default(object):

    def it_provides_read_access_to_xml_values(self):
        default = a_Default().element
        assert default.extension == 'xml'
        assert default.content_type == 'application/xml'


class DescribeCT_Override(object):

    def it_provides_read_access_to_xml_values(self):
        override = an_Override().element
        assert override.partname == '/part/name.xml'
        assert override.content_type == 'app/vnd.type'


class DescribeCT_Relationship(object):

    def it_provides_read_access_to_xml_values(self):
        rel = a_Relationship().element
        assert rel.rId == 'rId9'
        assert rel.reltype == 'ReLtYpE'
        assert rel.target_ref == 'docProps/core.xml'
        assert rel.target_mode == RTM.INTERNAL
