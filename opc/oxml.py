# -*- coding: utf-8 -*-
#
# oxml.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Classes that directly manipulate Open XML and provide direct object-oriented
access to the XML elements.
"""

from lxml import etree, objectify

from opc.constants import NAMESPACE as NS, RELATIONSHIP_TARGET_MODE as RTM


# configure objectified XML parser
fallback_lookup = objectify.ObjectifyElementClassLookup()
element_class_lookup = etree.ElementNamespaceClassLookup(fallback_lookup)
oxml_parser = etree.XMLParser(remove_blank_text=True)
oxml_parser.set_element_class_lookup(element_class_lookup)

nsmap = {
    'ct': NS.OPC_CONTENT_TYPES,
    'pr': NS.OPC_RELATIONSHIPS,
}


# ===========================================================================
# functions
# ===========================================================================

def oxml_fromstring(text):
    """``etree.fromstring()`` replacement that uses oxml parser"""
    return objectify.fromstring(text, oxml_parser)


def oxml_tostring(elm, encoding=None, pretty_print=False, standalone=None):
    # if xsi parameter is not set to False, PowerPoint won't load without a
    # repair step; deannotate removes some original xsi:type tags in core.xml
    # if this parameter is left out (or set to True)
    objectify.deannotate(elm, xsi=False, cleanup_namespaces=True)
    return etree.tostring(elm, encoding=encoding, pretty_print=pretty_print,
                          standalone=standalone)


# ===========================================================================
# Custom element classes
# ===========================================================================

class OxmlBaseElement(objectify.ObjectifiedElement):
    """
    Base class for all custom element classes, to add standardized behavior
    to all classes in one place.
    """
    @property
    def xml(self):
        """
        Return XML string for this element, suitable for testing purposes.
        Pretty printed for readability and without an XML declaration at the
        top.
        """
        return oxml_tostring(self, encoding='unicode', pretty_print=True)


class CT_Default(OxmlBaseElement):
    """
    ``<Default>`` element, specifying the default content type to be applied
    to a part with the specified extension.
    """
    @property
    def content_type(self):
        """
        String held in the ``ContentType`` attribute of this ``<Default>``
        element.
        """
        return self.get('ContentType')

    @property
    def extension(self):
        """
        String held in the ``Extension`` attribute of this ``<Default>``
        element.
        """
        return self.get('Extension')


class CT_Relationship(OxmlBaseElement):
    """
    ``<Relationship>`` element, representing a single relationship from a
    source to a target part.
    """
    @property
    def rId(self):
        """
        String held in the ``Id`` attribute of this ``<Relationship>``
        element.
        """
        return self.get('Id')

    @property
    def reltype(self):
        """
        String held in the ``Type`` attribute of this ``<Relationship>``
        element.
        """
        return self.get('Type')

    @property
    def target_ref(self):
        """
        String held in the ``Target`` attribute of this ``<Relationship>``
        element.
        """
        return self.get('Target')

    @property
    def target_mode(self):
        """
        String held in the ``TargetMode`` attribute of this
        ``<Relationship>`` element, either ``Internal`` or ``External``.
        Defaults to ``Internal``.
        """
        return self.get('TargetMode', RTM.INTERNAL)


ct_namespace = element_class_lookup.get_namespace(nsmap['ct'])
ct_namespace['Default'] = CT_Default
pr_namespace = element_class_lookup.get_namespace(nsmap['pr'])
pr_namespace['Relationship'] = CT_Relationship
