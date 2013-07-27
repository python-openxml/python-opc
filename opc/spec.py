# -*- coding: utf-8 -*-
#
# spec.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of python-opc and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Provides mappings that embody aspects of the Open XML spec ISO/IEC 29500.
"""

from opc.constants import CONTENT_TYPE as CT


default_content_types = (
    ('.bin',     CT.PML_PRINTER_SETTINGS),
    ('.bin',     CT.SML_PRINTER_SETTINGS),
    ('.bin',     CT.WML_PRINTER_SETTINGS),
    ('.bmp',     CT.BMP),
    ('.emf',     CT.X_EMF),
    ('.fntdata', CT.X_FONTDATA),
    ('.gif',     CT.GIF),
    ('.jpe',     CT.JPEG),
    ('.jpeg',    CT.JPEG),
    ('.jpg',     CT.JPEG),
    ('.png',     CT.PNG),
    ('.rels',    CT.OPC_RELATIONSHIPS),
    ('.tif',     CT.TIFF),
    ('.tiff',    CT.TIFF),
    ('.wdp',     CT.MS_PHOTO),
    ('.wmf',     CT.X_WMF),
    ('.xlsx',    CT.SML_SHEET),
    ('.xml',     CT.XML),
)
