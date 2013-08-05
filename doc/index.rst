##########
python-opc
##########

Welcome
=======

|po| is a Python library for manipulating Open Packaging Convention (OPC)
packages. An OPC package is the file format used by Microsoft Office 2007 and
later for Word, Excel, and PowerPoint.

**STATUS: as of Jul 28 2013 python-opc and this documentation for it are both
work in progress.**


Documentation
=============

|OpcPackage| objects
====================

.. autoclass:: opc.OpcPackage
   :members:
   :member-order: bysource
   :undoc-members:


|Part| objects
==============

The |Part| class is the default type for package parts and also serves as the
base class for custom part classes.

.. autoclass:: opc.package.Part
   :members:
   :member-order: bysource
   :undoc-members:


|_Relationship| objects
=======================

The |_Relationship| class ...

.. autoclass:: opc.package._Relationship
   :members:
   :member-order: bysource
   :undoc-members:


Concepts
========

ISO/IEC 29500 Specification
---------------------------


Package contents
----------------

Content types stream, package relationships, parts.


Pack URIs
---------

... A partname is a special case of pack URI ...


Parts
-----


Relationships
-------------

... target mode ... relationship type ... rId ... targets


Content types
-------------



Contents
========

.. toctree::
   content_types
   relationship_types
   developer/design_narratives
   :maxdepth: 2

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

