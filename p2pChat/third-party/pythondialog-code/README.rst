===============================================================================
Python wrapper for the UNIX "dialog" utility
===============================================================================
Easy writing of graphical interfaces for terminal-based applications
-------------------------------------------------------------------------------

Overview
--------

pythondialog is a Python wrapper for the UNIX dialog_ utility
originally written by Savio Lam and later rewritten by Thomas E. Dickey.
Its purpose is to provide an easy to use, pythonic and as complete as
possible interface to dialog_ from Python code.

.. _dialog: https://invisible-island.net/dialog/dialog.html

pythondialog is free software, licensed under the GNU LGPL (GNU Lesser
General Public License). Its home page is located at:

  http://pythondialog.sourceforge.net/

and contains a `short example`_, screenshots_, a `summary of the recent
changes`_, links to the `documentation`_, the `Git repository`_, the
`mailing list`_, the `issue tracker`_, etc.

.. _short example:  http://pythondialog.sourceforge.net/#example
.. _screenshots:    http://pythondialog.sourceforge.net/gallery.html
.. _summary of the recent changes:
                    http://pythondialog.sourceforge.net/news.html
.. _documentation:  http://pythondialog.sourceforge.net/doc/
.. _Git repository: https://sourceforge.net/p/pythondialog/code/
.. _mailing list:   https://sourceforge.net/p/pythondialog/mailman/
.. _issue tracker:  https://sourceforge.net/p/pythondialog/_list/tickets

If you want to get a quick idea of what this module allows one to do,
you can download a release tarball and run ``demo.py``::

  PYTHONPATH=. python3 examples/demo.py


What is pythondialog good for? What are its limitations?
--------------------------------------------------------

As you might infer from the name, dialog is a high-level program that
generates dialog boxes. So is pythondialog. They allow you to build nice
interfaces quickly and easily, but you don't have full control over the
widgets, nor can you create new widgets without modifying dialog itself.
If you need to do low-level stuff, you should have a look at `ncurses`_
(cf. the ``curses`` module in the Python standard library), `blessings`_
or slang instead. For sophisticated text-mode interfaces, the `Urwid
Python library`_ looks rather interesting, too.

.. _ncurses: https://invisible-island.net/ncurses/ncurses.html
.. _blessings: https://github.com/erikrose/blessings
.. _Urwid Python library: http://excess.org/urwid/


Requirements
------------

* As of version 2.12, the reference implementation of pythondialog
  (which this file belongs to) requires Python 3.0 or later in the 3.x
  series. pythondialog 3.5.1 has been tested with Python 3.8.

* Versions of pythondialog up to and including 3.5.1 had a backport to
  Python 2, however this outdated Python dialect isn't supported
  anymore. You may find pointers to the old packages with Python 2
  support on the `pythondialog home page`_.

  .. _pythondialog home page: http://pythondialog.sourceforge.net/

* Apart from that, pythondialog requires the dialog_ program (or a
  drop-in replacement for dialog). You can download dialog from:

    https://invisible-island.net/dialog/dialog.html

  Note that some features of pythondialog may require recent versions of
  dialog.


Quick installation instructions
-------------------------------

If you have a working `pip <https://pypi.org/project/pip/>`_ setup,
you should be able to install pythondialog with::

  pip install pythondialog

When doing so, make sure that your ``pip`` executable runs with the
Python 3 installation you want to install pythondialog for.

For more detailed instructions, you can read the ``INSTALL`` file from a
release tarball. You may also want to consult the `pip documentation
<https://pip.pypa.io/>`_.


Documentation
-------------

The pythondialog Manual
^^^^^^^^^^^^^^^^^^^^^^^

The pythondialog Manual is written in `reStructuredText`_ format for the
`Sphinx`_ documentation generator. The HTML documentation for the latest
version of pythondialog as rendered by Sphinx should be available at:

  http://pythondialog.sourceforge.net/doc/

.. _pythondialog Manual: http://pythondialog.sourceforge.net/doc/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _LaTeX: https://www.latex-project.org/
.. _Make: https://www.gnu.org/software/make/

The sources for the pythondialog Manual are located in the ``doc``
top-level directory of the pythondialog distribution, but the
documentation build process pulls many parts from ``dialog.py`` (mainly
docstrings).

To generate the documentation yourself from ``dialog.py`` and the
sources in the ``doc`` directory, first make sure you have `Sphinx`_ and
`Make`_ installed. Then, you can go to the ``doc`` directory and type,
for instance::

  make html

You will then find the output in the ``_build/html`` subdirectory of
``doc``. `Sphinx`_ can build the documentation in many other formats.
For instance, if you have `LaTeX`_ installed, you can generate the
pythondialog Manual in PDF format using::

  make latexpdf

You can run ``make`` from the ``doc`` directory to see a list of the
available formats. Run ``make clean`` to clean up after the
documentation build process.

For those who have installed `Sphinx`_ but not `Make`_, it is still
possible to build the documentation with a command such as::

  sphinx-build -b html . _build/html

run from the ``doc`` directory. Please refer to `sphinx-build`_ for more
details.

.. _sphinx-build: https://www.sphinx-doc.org/en/master/man/sphinx-build.html


Reading the docstrings from an interactive Python interpreter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have already installed pythondialog, you may consult its
docstrings in an interactive Python interpreter this way::

   >>> import dialog; help(dialog)

but only parts of the documentation are available using this method, and
the result is much less convenient to use than the `pythondialog
Manual`_ as generated by `Sphinx`_.


Enabling Deprecation Warnings
-----------------------------

There are a few places in ``dialog.py`` that send a
``DeprecationWarning`` to warn developers about obsolete features.
However, because of:

  - the dialog output to the terminal;
  - the fact that such warnings are silenced by default since Python 2.7
    and 3.2;

you have to do two things in order to see them:

  - redirect the standard error stream to a file;
  - enable the warnings for the Python interpreter.

For instance, to see the warnings produced when running the demo, you
can do::

  PYTHONPATH=. python3 -Wd examples/demo.py 2>/path/to/file

and examine ``/path/to/file``. This can also help you to find files that
are still open when your program exits.

**Note:**

  If your program is terminated by an unhandled exception while stderr
  is redirected as in the preceding command, you won't see the traceback
  until you examine the file stderr was redirected to. This can be
  disturbing, as your program may exit with no apparent reason in such
  conditions.

For more explanations and other methods to enable deprecation warnings,
please refer to:

  https://docs.python.org/3/whatsnew/2.7.html


Troubleshooting
---------------

If you have a problem with a pythondialog call, you should read its
documentation and the dialog(1) manual page. If this is not enough, you
can enable logging of shell command-line equivalents of all dialog calls
made by your program with a simple call to ``Dialog.setup_debug()``,
first available in pythondialog 2.12 (the ``expand_file_opt`` parameter
may be useful in versions 3.3 and later). An example of this can be
found in ``demo.py`` from the ``examples`` directory.

As of version 2.12, you can also enable this debugging facility for
``demo.py`` by calling it with the ``--debug`` flag (possibly combined
with ``--debug-expand-file-opt`` in pythondialog 3.3 and later, cf.
``demo.py --help``).


Using Xdialog instead of dialog
-------------------------------

As far as I can tell, `Xdialog`_ has not been ported to `GTK+`_ version
2 or later. It is not in `Debian`_ stable nor unstable (November 30, 2019).
It is not installed on my system (because of the GTK+ 1.2 dependency),
and according to the Xdialog-specific patches I received from Peter
Åstrand in 2004, was not a drop-in replacement for `dialog`_ (in
particular, Xdialog seemed to want to talk to the caller through stdout
instead of stderr, grrrrr!).

.. _Xdialog: http://xdialog.free.fr/
.. _GTK+: https://www.gtk.org/
.. _Debian: https://www.debian.org/

All this to say that, even though I didn't remove the options to use
another backend than dialog, nor did I remove the handful of little,
non-invasive modifications that help pythondialog work better with
`Xdialog`_, I don't really support the latter. I test everything with
dialog, and nothing with Xdialog.

That being said, here is the *old* text of this section (from 2004), in
case you are still interested:

  Starting with 2.06, there is an "Xdialog" compatibility mode that you
  can use if you want pythondialog to run the graphical Xdialog program
  (which *should* be found under http://xdialog.free.fr/) instead of
  dialog (text-mode, based on the ncurses library).

  The primary supported platform is still dialog, but as long as only
  small modifications are enough to make pythondialog work with Xdialog,
  I am willing to support Xdialog if people are interested in it (which
  turned out to be the case for Xdialog).

  The demo.py from pythondialog 2.06 has been tested with Xdialog 2.0.6
  and found to work well (barring Xdialog's annoying behaviour with the
  file selection dialog box).


Whiptail, anyone?
-----------------

Well, pythondialog seems not to work very well with whiptail. The reason
is that whiptail is not compatible with dialog anymore. Although you can
tell pythondialog the program you want it to invoke, only programs that
are mostly dialog-compatible are supported.


History
-------

pythondialog was originally written by Robb Shecter. Sultanbek Tezadov
added some features to it (mainly the first gauge implementation, I
guess). Florent Rougon rewrote most parts of the program to make it more
robust and flexible so that it can give access to most features of the
dialog program. Peter Åstrand took over maintainership between 2004 and
2009, with particular care for the `Xdialog`_ support. Florent Rougon
took over maintainership again starting from 2009...

.. 
  # Local Variables:
  # coding: utf-8
  # fill-column: 72
  # End:
