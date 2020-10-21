.. meta::
   :description: pythondialog's documentation
   :keywords: pythondialog, Python, dialog, ncurses, Xdialog, terminal-based
              interface, text-mode interface, manual

###################
pythondialog Manual
###################

.. module:: dialog
   :synopsis: A Python interface to the UNIX dialog utility and mostly-compatible programs
   :platform: Unix
.. codeauthor:: Florent Rougon
.. codeauthor:: Robb Shecter
.. codeauthor:: Peter Åstrand
.. codeauthor:: Sultanbek Tezadov
.. sectionauthor:: Florent Rougon

This manual documents pythondialog_, a Python wrapper for the dialog_
utility originally written by Savio Lam, and later rewritten by Thomas
E. Dickey. Its purpose is to provide an easy to use, pythonic and
comprehensive Python interface to :program:`dialog`. This allows one to make
simple text-mode user interfaces on Unix-like systems.

.. _pythondialog: http://pythondialog.sourceforge.net/
.. _dialog: https://invisible-island.net/dialog/dialog.html

pythondialog's functionality is contained within the :mod:`dialog` Python
module. This module doesn't contain much Unix-specific code, if
any; however, its backend of reference, which is the :program:`dialog`
program, only works on Unix-like platforms so far as I can tell. Given a
suitable backend, the :mod:`dialog` module could work on other platforms.


*************
Main Contents
*************

.. toctree::
   :maxdepth: 2

   intro/intro
   Dialog_class_overview
   widgets
   DialogBackendVersion
   exceptions
   internals

.. reference

.. Either this, or use the “orphan” metadata since I don't want the glossary
.. to appear in the table of contents.
.. toctree::
   :hidden:

   glossary


**********
Appendices
**********

* :ref:`glossary`
* :ref:`genindex`
* :ref:`search`
