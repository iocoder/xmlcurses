XMLCurses
=========

.. contents:: Table of Contents:
   :local:

Introduction
------------

This package serves as an easy-to-use interface for Python's curses library. The goal of XMLCurses
is to allow Python programmers describe their desired layourt for curses windows in a simple
way, using XML files.

Requirements
-------------

* Python -- one of the following:

  - CPython_ >= 2.6 or >= 3.3
  - PyPy_ >= 4.0
  - IronPython_ 2.7

.. _CPython: http://www.python.org/
.. _PyPy: http://pypy.org/
.. _IronPython: http://ironpython.net/

Installation
------------

The last stable release is available on PyPI and can be installed with ``pip``::

    $ sudo pip install xmlcurses

Documentation
-------------

Documentation is available online: http://xmlcurses.readthedocs.io/

Code Examples
-------------

To execute the code examples provided in the source code, execute::

    $ make run EXAMPLE='exampleName'

Replace 'exampleName' with msgwin, inputwin, or tblwin. 

License
-------

XMLCurses is released under GNU GPL v3.0. See LICENSE for more information.

