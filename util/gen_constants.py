#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gen_constants.py
#
# Generate the constant definitions for opc/constants.py from an XML source
# document. The constant names are calculated using the last part of the
# content type or relationship type string.

import os

from lxml import objectify


# calculate absolute path to xml file
thisdir = os.path.split(__file__)[0]
xml_relpath = 'src_data/part-types.xml'
xml_path = os.path.join(thisdir, xml_relpath)


def content_types_documentation_page(xml_path):
    """
    Generate restructuredText (rst) documentation for content type constants.
    """
    print '###########################'
    print 'Content type constant names'
    print '###########################'
    content_types = parse_content_types(xml_path)
    for name in sorted(content_types.keys()):
        print '\n%s' % name
        print '    %s' % content_types[name]


def relationship_types_documentation_page(xml_path):
    """
    Generate restructuredText (rst) documentation for relationship type
    constants.
    """
    print '################################'
    print 'Relationship type constant names'
    print '################################'
    relationship_types = parse_relationship_types(xml_path)
    for name in sorted(relationship_types.keys()):
        print '\n%s' % name
        print '    \\%s' % relationship_types[name]


def content_type_constant_names(xml_path):
    """
    Calculate constant names for content types in source XML document
    """
    print '\n\nclass CONTENT_TYPE(object):'
    content_types = parse_content_types(xml_path)
    for name in sorted(content_types.keys()):
        content_type = content_types[name]
        print '    %s = (' % name
        print '        \'%s\'' % content_type[:67]
        if len(content_type) > 67:
            print '        \'%s\'' % content_type[67:]
        print '    )'


def relationship_type_constant_names(xml_path):
    """
    Calculate constant names for relationship types in source XML document
    """
    print '\n\nclass RELATIONSHIP_TYPE(object):'
    relationship_types = parse_relationship_types(xml_path)
    for name in sorted(relationship_types.keys()):
        relationship_type = relationship_types[name]
        print '    %s = (' % name
        print '        \'%s\'' % relationship_type[:67]
        if len(relationship_type) > 67:
            print '        \'%s\'' % relationship_type[67:]
        print '    )'


def parse_content_types(xml_path):
    content_types = {}
    root = objectify.parse(xml_path).getroot()
    for part in root.iterchildren('*'):
        content_type = str(part.ContentType)
        if content_type.startswith('Any '):
            continue
        name = const_name(content_type)
        content_types[name] = content_type
    return content_types


def parse_relationship_types(xml_path):
    relationship_types = {}
    root = objectify.parse(xml_path).getroot()
    for part in root.iterchildren('*'):
        relationship_type = str(part.SourceRelationship)
        if relationship_type == '':
            continue
        name = rel_const_name(relationship_type)
        if (name in relationship_types and
                relationship_type != relationship_types[name]):
            raise ValueError(
                '%s, %s, %s' % (name, relationship_type,
                relationship_types[name])
            )
        relationship_types[name] = relationship_type
    return relationship_types


def const_name(content_type):
    prefix, camel_name = transform_prefix(content_type)
    return format_const_name(prefix, camel_name)


def rel_const_name(relationship_type):
    camel_name = rel_type_camel_name(relationship_type)
    return format_rel_const_name(camel_name)


def format_const_name(prefix, camel_name):
    camel_name = legalize_name(camel_name)
    snake_name = camel_to_snake(camel_name)
    tmpl = '%s_%s' if prefix else '%s%s'
    return tmpl % (prefix, snake_name.upper())


def format_rel_const_name(camel_name):
    camel_name = legalize_name(camel_name)
    snake_name = camel_to_snake(camel_name)
    return snake_name.upper()


def legalize_name(name):
    """
    Replace illegal variable name characters with underscore.
    """
    legal_name = ''
    for char in name:
        if char in '.-':
            char = '_'
        legal_name += char
    return legal_name


def camel_to_snake(camel_str):
    snake_str = ''
    for char in camel_str:
        if char.isupper():
            snake_str += '_'
        snake_str += char.lower()
    return snake_str


def transform_prefix(content_type):
    namespaces = (
        ('application/vnd.openxmlformats-officedocument.drawingml.',
         'DML'),
        ('application/vnd.openxmlformats-officedocument.presentationml.',
         'PML'),
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.',
         'SML'),
        ('application/vnd.openxmlformats-officedocument.wordprocessingml.',
         'WML'),
        ('application/vnd.openxmlformats-officedocument.',
         'OFC'),
        ('application/vnd.openxmlformats-package.',
         'OPC'),
        ('application/', ''),
        ('image/vnd.', ''),
        ('image/', ''),
    )
    for prefix, new_prefix in namespaces:
        if content_type.startswith(prefix):
            start = len(prefix)
            camel_name = content_type[start:]
            if camel_name.endswith('+xml'):
                camel_name = camel_name[:-4]
            return (new_prefix, camel_name)
    return ('', content_type)


def rel_type_camel_name(relationship_type):
    namespaces = (
        ('http://schemas.openxmlformats.org/officeDocument/2006/relationship'
         's/metadata/'),
        ('http://schemas.openxmlformats.org/officeDocument/2006/relationship'
         's/spreadsheetml/'),
        ('http://schemas.openxmlformats.org/officeDocument/2006/relationship'
         's/'),
        ('http://schemas.openxmlformats.org/package/2006/relationships/metad'
         'ata/'),
        ('http://schemas.openxmlformats.org/package/2006/relationships/digit'
         'al-signature/'),
        ('http://schemas.openxmlformats.org/package/2006/relationships/'),
    )
    for namespace in namespaces:
        if relationship_type.startswith(namespace):
            start = len(namespace)
            camel_name = relationship_type[start:]
            return camel_name
    return relationship_type


content_type_constant_names(xml_path)
relationship_type_constant_names(xml_path)
content_types_documentation_page(xml_path)
relationship_types_documentation_page(xml_path)
