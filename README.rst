##########
python-opc
##########

VERSION: 0.0.1d (first development release)


STATUS (as of June 23 2013)
===========================

First development release. Under active development.


Vision
======

A robust, general-purpose library for manipulating Open Packaging Convention
(OPC) packages, suitable as a foundation for a family of Open XML document
libraries. Also to be suitable for general purpose manipulation of OPC
packages, for example to access the XML and binary contents for indexing
purposes and perhaps for manipulating package parts, for example to remove
slide notes pages or to assemble presentations from individual slides in a
library.


Documentation
=============

Documentation is hosted on Read The Docs (readthedocs.org) at
https://python-opc.readthedocs.org/en/latest/.


Reaching out
============

We'd love to hear from you if you like |po|, want a new feature, find a bug,
need help using it, or just have a word of encouragement.

The **mailing list** for |po| is (google groups ... )

The **issue tracker** is on github at `python-openxml/python-opc`_.

Feature requests are best broached initially on the mailing list, they can be
added to the issue tracker once we've clarified the best approach,
particularly the appropriate API signature.

.. _`python-openxml/python-opc`:
   https://github.com/python-openxml/python-opc


Installation
============

|po| may be installed with ``pip`` if you have it available::

    pip install python-opc

It can also be installed using ``easy_install``::

    easy_install python-opc

If neither ``pip`` nor ``easy_install`` is available, it can be installed
manually by downloading the distribution from PyPI, unpacking the tarball,
and running ``setup.py``::

    tar xvzf python-opc-0.0.1d1.tar.gz
    cd python-opc-0.0.1d1
    python setup.py install

|po| depends on the ``lxml`` package. Both ``pip`` and ``easy_install`` will
take care of satisfying that dependency for you, but if you use this last
method you will need to install ``lxml`` yourself.


Release History
===============

June 23, 2013 - v0.0.1d1
   * Establish initial enviornment and development branches


License
=======

Licensed under the `MIT license`_. Short version: this code is copyrighted by
me (Steve Canny), I give you permission to do what you want with it except
remove my name from the credits. See the LICENSE file for specific terms.

.. _MIT license:
   http://www.opensource.org/licenses/mit-license.php

.. |po| replace:: ``python-opc``
