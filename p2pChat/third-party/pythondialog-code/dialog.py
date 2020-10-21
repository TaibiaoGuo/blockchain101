# dialog.py --- A Python interface to the ncurses-based "dialog" utility
# -*- coding: utf-8 -*-
#
# Copyright (C) 2002-2019  Florent Rougon
# Copyright (C) 2004  Peter Åstrand
# Copyright (C) 2000  Robb Shecter, Sultanbek Tezadov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA  02110-1301 USA.

"""Python interface to :program:`dialog`-like programs.

This module provides a Python interface to :program:`dialog`-like
programs such as :program:`dialog` and :program:`Xdialog`.

It provides a :class:`Dialog` class that retains some parameters such as
the program name and path as well as the values to pass as DIALOG*
environment variables to the chosen program.

See the pythondialog manual for detailed documentation.

"""

import collections
import os
import random
import re
import sys
import tempfile
import traceback
import warnings
from contextlib import contextmanager
from textwrap import dedent

_VersionInfo = collections.namedtuple(
    "VersionInfo", ("major", "minor", "micro", "releasesuffix"))

class VersionInfo(_VersionInfo):
    """Class used to represent the version of pythondialog.

    This class is based on :func:`collections.namedtuple` and has the
    following field names: ``major``, ``minor``, ``micro``,
    ``releasesuffix``.

    .. versionadded:: 2.14
    """
    def __str__(self):
        """Return a string representation of the version."""
        res = ".".join( ( str(elt) for elt in self[:3] ) )
        if self.releasesuffix:
            res += self.releasesuffix
        return res

    def __repr__(self):
        return "{0}.{1}".format(__name__, _VersionInfo.__repr__(self))

#: Version of pythondialog as a :class:`VersionInfo` instance.
#:
#: .. versionadded:: 2.14
version_info = VersionInfo(3, 5, 1, None)
#: Version of pythondialog as a string.
#:
#: .. versionadded:: 2.12
__version__ = str(version_info)


# This is not for calling programs, only to prepare the shell commands that are
# written to the debug log when debugging is enabled.
try:
    from shlex import quote as _shell_quote
except ImportError:
    def _shell_quote(s):
        return "'%s'" % s.replace("'", "'\"'\"'")


# Exceptions raised by this module
#
# When adding, suppressing, renaming exceptions or changing their
# hierarchy, don't forget to update the module's docstring.
class error(Exception):
    """Base class for exceptions in pythondialog."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.complete_message()

    def __repr__(self):
        return "{0}.{1}({2!r})".format(__name__, self.__class__.__name__,
                                       self.message)

    def complete_message(self):
        if self.message:
            return "{0}: {1}".format(self.ExceptionShortDescription,
                                     self.message)
        else:
            return self.ExceptionShortDescription

    ExceptionShortDescription = "{0} generic exception".format("pythondialog")

# For backward-compatibility
#
# Note: this exception was not documented (only the specific ones were), so
#       the backward-compatibility binding could be removed relatively easily.
PythonDialogException = error

class ExecutableNotFound(error):
    """Exception raised when the :program:`dialog` executable can't be found."""
    ExceptionShortDescription = "Executable not found"

class PythonDialogBug(error):
    """Exception raised when pythondialog finds a bug in his own code."""
    ExceptionShortDescription = "Bug in pythondialog"

# Yeah, the "Probably" makes it look a bit ugly, but:
#   - this is more accurate
#   - this avoids a potential clash with an eventual PythonBug built-in
#     exception in the Python interpreter...
class ProbablyPythonBug(error):
    """Exception raised when pythondialog behaves in a way that seems to \
indicate a Python bug."""
    ExceptionShortDescription = "Bug in python, probably"

class BadPythonDialogUsage(error):
    """Exception raised when pythondialog is used in an incorrect way."""
    ExceptionShortDescription = "Invalid use of pythondialog"

class PythonDialogSystemError(error):
    """Exception raised when pythondialog cannot perform a "system \
operation" (e.g., a system call) that should work in "normal" situations.

    This is a convenience exception: :exc:`PythonDialogIOError`,
    :exc:`PythonDialogOSError` and
    :exc:`PythonDialogErrorBeforeExecInChildProcess` all derive from
    this exception. As a consequence, watching for
    :exc:`PythonDialogSystemError` instead of the aformentioned
    exceptions is enough if you don't need precise details about these
    kinds of errors.

    Don't confuse this exception with Python's builtin
    :exc:`SystemError` exception.

    """
    ExceptionShortDescription = "System error"

class PythonDialogOSError(PythonDialogSystemError):
    """Exception raised when pythondialog catches an :exc:`OSError` exception \
that should be passed to the calling program."""
    ExceptionShortDescription = "OS error"

class PythonDialogIOError(PythonDialogOSError):
    """Exception raised when pythondialog catches an :exc:`IOError` exception \
that should be passed to the calling program.

    This exception should not be raised starting from Python 3.3, as the
    built-in exception :exc:`IOError` becomes an alias of
    :exc:`OSError`.

    .. versionchanged:: 2.12
       :exc:`PythonDialogIOError` is now a subclass of
       :exc:`PythonDialogOSError` in order to help with the transition
       from :exc:`IOError` to :exc:`OSError` in the Python language.
       With this change, you can safely replace ``except
       PythonDialogIOError`` clauses with ``except PythonDialogOSError``
       even if running under Python < 3.3.

    """
    ExceptionShortDescription = "IO error"

class PythonDialogErrorBeforeExecInChildProcess(PythonDialogSystemError):
    """Exception raised when an exception is caught in a child process \
before the exec sytem call (included).

    This can happen in uncomfortable situations such as:

      - the system being out of memory;
      - the maximum number of open file descriptors being reached;
      - the :program:`dialog`-like program being removed (or made
        non-executable) between the time we found it with
        :func:`_find_in_path` and the time the exec system call
        attempted to execute it;
      - the Python program trying to call the :program:`dialog`-like
        program with arguments that cannot be represented in the user's
        locale (:envvar:`LC_CTYPE`).

    """
    ExceptionShortDescription = "Error in a child process before the exec " \
                                "system call"

class PythonDialogReModuleError(PythonDialogSystemError):
    """Exception raised when pythondialog catches a :exc:`re.error` exception."""
    ExceptionShortDescription = "'re' module error"

class UnexpectedDialogOutput(error):
    """Exception raised when the :program:`dialog`-like program returns \
something not expected by pythondialog."""
    ExceptionShortDescription = "Unexpected dialog output"

class DialogTerminatedBySignal(error):
    """Exception raised when the :program:`dialog`-like program is \
terminated by a signal."""
    ExceptionShortDescription = "dialog-like terminated by a signal"

class DialogError(error):
    """Exception raised when the :program:`dialog`-like program exits \
with the code indicating an error."""
    ExceptionShortDescription = "dialog-like terminated due to an error"

class UnableToRetrieveBackendVersion(error):
    """Exception raised when we cannot retrieve the version string of the \
:program:`dialog`-like backend.

    .. versionadded:: 2.14
    """
    ExceptionShortDescription = "Unable to retrieve the version of the \
dialog-like backend"

class UnableToParseBackendVersion(error):
    """Exception raised when we cannot parse the version string of the \
:program:`dialog`-like backend.

    .. versionadded:: 2.14
    """
    ExceptionShortDescription = "Unable to parse as a dialog-like backend \
version string"

class UnableToParseDialogBackendVersion(UnableToParseBackendVersion):
    """Exception raised when we cannot parse the version string of the \
:program:`dialog` backend.

    .. versionadded:: 2.14
    """
    ExceptionShortDescription = "Unable to parse as a dialog version string"

class InadequateBackendVersion(error):
    """Exception raised when the backend version in use is inadequate \
in a given situation.

    .. versionadded:: 2.14
    """
    ExceptionShortDescription = "Inadequate backend version"


@contextmanager
def _OSErrorHandling():
    try:
        yield
    except OSError as e:
        raise PythonDialogOSError(str(e)) from e
    except IOError as e:
        raise PythonDialogIOError(str(e)) from e


try:
    # Values accepted for checklists
    _on_cre = re.compile(r"on$", re.IGNORECASE)
    _off_cre = re.compile(r"off$", re.IGNORECASE)

    _calendar_date_cre = re.compile(
        r"(?P<day>\d\d)/(?P<month>\d\d)/(?P<year>\d\d\d\d)$")
    _timebox_time_cre = re.compile(
        r"(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)$")
except re.error as e:
    raise PythonDialogReModuleError(str(e)) from e


# From dialog(1):
#
#   All options begin with "--" (two ASCII hyphens, for the benefit of those
#   using systems with deranged locale support).
#
#   A "--" by itself is used as an escape, i.e., the next token on the
#   command-line is not treated as an option, as in:
#        dialog --title -- --Not an option
def _dash_escape(args):
    """Escape all elements of *args* that need escaping.

    *args* may be any sequence and is not modified by this function.
    Return a new list where every element that needs escaping has been
    escaped.

    An element needs escaping when it starts with two ASCII hyphens
    (``--``). Escaping consists in prepending an element composed of two
    ASCII hyphens, i.e., the string ``'--'``.

    """
    res = []

    for arg in args:
        if arg.startswith("--"):
            res.extend(("--", arg))
        else:
            res.append(arg)

    return res

# We need this function in the global namespace for the lambda
# expressions in _common_args_syntax to see it when they are called.
def _dash_escape_nf(args):      # nf: non-first
    """Escape all elements of *args* that need escaping, except the first one.

    See :func:`_dash_escape` for details. Return a new list.

    """
    if not args:
        raise PythonDialogBug("not a non-empty sequence: {0!r}".format(args))
    l = _dash_escape(args[1:])
    l.insert(0, args[0])
    return l

def _simple_option(option, enable):
    """Turn on or off the simplest :term:`dialog common options`."""
    if enable:
        return (option,)
    else:
        # This will not add any argument to the command line
        return ()


# This dictionary allows us to write the dialog common options in a Pythonic
# way (e.g. dialog_instance.checklist(args, ..., title="Foo", no_shadow=True)).
#
# Options such as --separate-output should obviously not be set by the user
# since they affect the parsing of dialog's output:
_common_args_syntax = {
    "ascii_lines": lambda enable: _simple_option("--ascii-lines", enable),
    "aspect": lambda ratio: _dash_escape_nf(("--aspect", str(ratio))),
    "backtitle": lambda backtitle: _dash_escape_nf(("--backtitle", backtitle)),
    # Obsolete according to dialog(1)
    "beep": lambda enable: _simple_option("--beep", enable),
    # Obsolete according to dialog(1)
    "beep_after": lambda enable: _simple_option("--beep-after", enable),
    # Warning: order = y, x!
    "begin": lambda coords: _dash_escape_nf(
        ("--begin", str(coords[0]), str(coords[1]))),
    "cancel_label": lambda s: _dash_escape_nf(("--cancel-label", s)),
    # Old, unfortunate choice of key, kept for backward compatibility
    "cancel": lambda s: _dash_escape_nf(("--cancel-label", s)),
    "clear": lambda enable: _simple_option("--clear", enable),
    "colors": lambda enable: _simple_option("--colors", enable),
    "column_separator": lambda s: _dash_escape_nf(("--column-separator", s)),
    "cr_wrap": lambda enable: _simple_option("--cr-wrap", enable),
    "create_rc": lambda filename: _dash_escape_nf(("--create-rc", filename)),
    "date_format": lambda s: _dash_escape_nf(("--date-format", s)),
    "defaultno": lambda enable: _simple_option("--defaultno", enable),
    "default_button": lambda s: _dash_escape_nf(("--default-button", s)),
    "default_item": lambda s: _dash_escape_nf(("--default-item", s)),
    "exit_label": lambda s: _dash_escape_nf(("--exit-label", s)),
    "extra_button": lambda enable: _simple_option("--extra-button", enable),
    "extra_label": lambda s: _dash_escape_nf(("--extra-label", s)),
    "help": lambda enable: _simple_option("--help", enable),
    "help_button": lambda enable: _simple_option("--help-button", enable),
    "help_label": lambda s: _dash_escape_nf(("--help-label", s)),
    "help_status": lambda enable: _simple_option("--help-status", enable),
    "help_tags": lambda enable: _simple_option("--help-tags", enable),
    "hfile": lambda filename: _dash_escape_nf(("--hfile", filename)),
    "hline": lambda s: _dash_escape_nf(("--hline", s)),
    "ignore": lambda enable: _simple_option("--ignore", enable),
    "insecure": lambda enable: _simple_option("--insecure", enable),
    "item_help": lambda enable: _simple_option("--item-help", enable),
    "keep_tite": lambda enable: _simple_option("--keep-tite", enable),
    "keep_window": lambda enable: _simple_option("--keep-window", enable),
    "max_input": lambda size: _dash_escape_nf(("--max-input", str(size))),
    "no_cancel": lambda enable: _simple_option("--no-cancel", enable),
    "nocancel": lambda enable: _simple_option("--nocancel", enable),
    "no_collapse": lambda enable: _simple_option("--no-collapse", enable),
    "no_kill": lambda enable: _simple_option("--no-kill", enable),
    "no_label": lambda s: _dash_escape_nf(("--no-label", s)),
    "no_lines": lambda enable: _simple_option("--no-lines", enable),
    "no_mouse": lambda enable: _simple_option("--no-mouse", enable),
    "no_nl_expand": lambda enable: _simple_option("--no-nl-expand", enable),
    "no_ok": lambda enable: _simple_option("--no-ok", enable),
    "no_shadow": lambda enable: _simple_option("--no-shadow", enable),
    "no_tags": lambda enable: _simple_option("--no-tags", enable),
    "ok_label": lambda s: _dash_escape_nf(("--ok-label", s)),
    # cf. Dialog.maxsize()
    "print_maxsize": lambda enable: _simple_option("--print-maxsize",
                                                   enable),
    "print_size": lambda enable: _simple_option("--print-size", enable),
    # cf. Dialog.backend_version()
    "print_version": lambda enable: _simple_option("--print-version",
                                                   enable),
    "scrollbar": lambda enable: _simple_option("--scrollbar", enable),
    "separate_output": lambda enable: _simple_option("--separate-output",
                                                     enable),
    "separate_widget": lambda s: _dash_escape_nf(("--separate-widget", s)),
    "shadow": lambda enable: _simple_option("--shadow", enable),
    # Obsolete according to dialog(1)
    "size_err": lambda enable: _simple_option("--size-err", enable),
    "sleep": lambda secs: _dash_escape_nf(("--sleep", str(secs))),
    "stderr": lambda enable: _simple_option("--stderr", enable),
    "stdout": lambda enable: _simple_option("--stdout", enable),
    "tab_correct": lambda enable: _simple_option("--tab-correct", enable),
    "tab_len": lambda n: _dash_escape_nf(("--tab-len", str(n))),
    "time_format": lambda s: _dash_escape_nf(("--time-format", s)),
    "timeout": lambda secs: _dash_escape_nf(("--timeout", str(secs))),
    "title": lambda title: _dash_escape_nf(("--title", title)),
    "trace": lambda filename: _dash_escape_nf(("--trace", filename)),
    "trim": lambda enable: _simple_option("--trim", enable),
    "version": lambda enable: _simple_option("--version", enable),
    "visit_items": lambda enable: _simple_option("--visit-items", enable),
    "week_start": lambda start: _dash_escape_nf(
        ("--week-start", str(start) if isinstance(start, int) else start)),
    "yes_label": lambda s: _dash_escape_nf(("--yes-label", s)) }


def _find_in_path(prog_name):
    """Search an executable in the :envvar:`PATH`.

    If :envvar:`PATH` is not defined, the default path
    ``/bin:/usr/bin`` is used.

    Return a path to the file, or ``None`` if no file with a matching
    basename as well as read and execute permissions is found.

    Notable exception:

      :exc:`PythonDialogOSError`

    """
    with _OSErrorHandling():
        PATH = os.getenv("PATH", "/bin:/usr/bin") # see the execvp(3) man page
        for d in PATH.split(os.pathsep):
            file_path = os.path.join(d, prog_name)
            if os.path.isfile(file_path) \
               and os.access(file_path, os.R_OK | os.X_OK):
                return file_path
        return None


def _path_to_executable(f):
    """Find a path to an executable.

    Find a path to an executable, using the same rules as the POSIX
    exec*p() functions (see execvp(3) for instance).

    If *f* contains a ``/`` character, it must be a relative or absolute
    path to a file that has read and execute permissions. If *f* does
    not contain a ``/`` character, it is looked for according to the
    contents of the :envvar:`PATH` environment variable, which defaults
    to ``/bin:/usr/bin`` if unset.

    The return value is the result of calling :func:`os.path.realpath`
    on the path found according to the rules described in the previous
    paragraph.

    Notable exceptions:

      - :exc:`ExecutableNotFound`
      - :exc:`PythonDialogOSError`

    """
    with _OSErrorHandling():
        if '/' in f:
            if os.path.isfile(f) and os.access(f, os.R_OK | os.X_OK):
                res = f
            else:
                raise ExecutableNotFound("%s cannot be read and executed" % f)
        else:
            res = _find_in_path(f)
            if res is None:
                raise ExecutableNotFound(
                    "can't find the executable for the dialog-like "
                    "program")

    return os.path.realpath(res)


def _to_onoff(val):
    """Convert boolean expressions to ``"on"`` or ``"off"``.

    :return:
      - ``"on"`` if *val* is ``True``, a non-zero integer, ``"on"`` or
        any case variation thereof;
      - ``"off"`` if *val* is ``False``, ``0``, ``"off"`` or any case
        variation thereof.

    Notable exceptions:

      - :exc:`PythonDialogReModuleError`
      - :exc:`BadPythonDialogUsage`

    """
    if isinstance(val, (bool, int)):
        return "on" if val else "off"
    elif isinstance(val, str):
        try:
            if _on_cre.match(val):
                return "on"
            elif _off_cre.match(val):
                return "off"
        except re.error as e:
            raise PythonDialogReModuleError(str(e)) from e

    raise BadPythonDialogUsage("invalid boolean value: {0!r}".format(val))


def _compute_common_args(mapping):
    """Compute the list of arguments for :term:`dialog common options`.

    Compute a list of the command-line arguments to pass to
    :program:`dialog` from a keyword arguments dictionary for options
    listed as "common options" in the manual page for :program:`dialog`.
    These are the options that are not tied to a particular widget.

    This allows one to specify these options in a pythonic way, such
    as::

       d.checklist(<usual arguments for a checklist>,
                   title="...",
                   backtitle="...")

    instead of having to pass them with strings like ``"--title foo"``
    or ``"--backtitle bar"``.

    Notable exceptions: none

    """
    args = []
    for option, value in mapping.items():
        args.extend(_common_args_syntax[option](value))
    return args


# Classes for dealing with the version of dialog-like backend programs
if sys.hexversion >= 0x030200F0:
    import abc
    # Abstract base class
    class BackendVersion(metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def __str__(self):
            raise NotImplementedError()

        if sys.hexversion >= 0x030300F0:
            @classmethod
            @abc.abstractmethod
            def fromstring(cls, s):
                raise NotImplementedError()
        else:                   # for Python 3.2
            @abc.abstractclassmethod
            def fromstring(cls, s):
                raise NotImplementedError()

        @abc.abstractmethod
        def __lt__(self, other):
            raise NotImplementedError()

        @abc.abstractmethod
        def __le__(self, other):
            raise NotImplementedError()

        @abc.abstractmethod
        def __eq__(self, other):
            raise NotImplementedError()

        @abc.abstractmethod
        def __ne__(self, other):
            raise NotImplementedError()

        @abc.abstractmethod
        def __gt__(self, other):
            raise NotImplementedError()

        @abc.abstractmethod
        def __ge__(self, other):
            raise NotImplementedError()
else:
    class BackendVersion:
        pass


class DialogBackendVersion(BackendVersion):
    """Class representing possible versions of the :program:`dialog` backend.

    The purpose of this class is to make it easy to reliably compare
    between versions of the :program:`dialog` backend. It encapsulates
    the specific details of the backend versioning scheme to allow
    eventual adaptations to changes in this scheme without affecting
    external code.

    The version is represented by two components in this class: the
    :dfn:`dotted part` and the :dfn:`rest`. For instance, in the
    ``'1.2'`` version string, the dotted part is ``[1, 2]`` and the rest
    is the empty string. However, in version ``'1.2-20130902'``, the
    dotted part is still ``[1, 2]``, but the rest is the string
    ``'-20130902'``.

    Instances of this class can be created with the constructor by
    specifying the dotted part and the rest. Alternatively, an instance
    can be created from the corresponding version string (e.g.,
    ``'1.2-20130902'``) using the :meth:`fromstring` class method. This
    is particularly useful with the result of
    :samp:`{d}.backend_version()`, where *d* is a :class:`Dialog`
    instance. Actually, the main constructor detects if its first
    argument is a string and calls :meth:`!fromstring` in this case as a
    convenience. Therefore, all of the following expressions are valid
    to create a DialogBackendVersion instance::

      DialogBackendVersion([1, 2])
      DialogBackendVersion([1, 2], "-20130902")
      DialogBackendVersion("1.2-20130902")
      DialogBackendVersion.fromstring("1.2-20130902")

    If *bv* is a :class:`DialogBackendVersion` instance,
    :samp:`str({bv})` is a string representing the same version (for
    instance, ``"1.2-20130902"``).

    Two :class:`DialogBackendVersion` instances can be compared with the
    usual comparison operators (``<``, ``<=``, ``==``, ``!=``, ``>=``,
    ``>``). The algorithm is designed so that the following order is
    respected (after instanciation with :meth:`fromstring`)::

      1.2 < 1.2-20130902 < 1.2-20130903 < 1.2.0 < 1.2.0-20130902

    among other cases. Actually, the *dotted parts* are the primary keys
    when comparing and *rest* strings act as secondary keys. *Dotted
    parts* are compared with the standard Python list comparison and
    *rest* strings using the standard Python string comparison.

    """
    try:
        _backend_version_cre = re.compile(r"""(?P<dotted> (\d+) (\.\d+)* )
                                              (?P<rest>.*)$""", re.VERBOSE)
    except re.error as e:
        raise PythonDialogReModuleError(str(e)) from e

    def __init__(self, dotted_part_or_str, rest=""):
        """Create a :class:`DialogBackendVersion` instance.

        Please see the class docstring for details.

        """
        if isinstance(dotted_part_or_str, str):
            if rest:
                raise BadPythonDialogUsage(
                    "non-empty 'rest' with 'dotted_part_or_str' as string: "
                    "{0!r}".format(rest))
            else:
                tmp = self.__class__.fromstring(dotted_part_or_str)
                dotted_part_or_str, rest = tmp.dotted_part, tmp.rest

        for elt in dotted_part_or_str:
            if not isinstance(elt, int):
                raise BadPythonDialogUsage(
                    "when 'dotted_part_or_str' is not a string, it must "
                    "be a sequence (or iterable) of integers; however, "
                    "{0!r} is not an integer.".format(elt))

        self.dotted_part = list(dotted_part_or_str)
        self.rest = rest

    def __repr__(self):
        return "{0}.{1}({2!r}, rest={3!r})".format(
            __name__, self.__class__.__name__, self.dotted_part, self.rest)

    def __str__(self):
        return '.'.join(map(str, self.dotted_part)) + self.rest

    @classmethod
    def fromstring(cls, s):
        """Create a :class:`DialogBackendVersion` instance from a \
:program:`dialog` version string.

        :param str s: a :program:`dialog` version string
        :return:
          a :class:`DialogBackendVersion` instance representing the same
          string

        Notable exceptions:

          - :exc:`UnableToParseDialogBackendVersion`
          - :exc:`PythonDialogReModuleError`

          """
        try:
            mo = cls._backend_version_cre.match(s)
            if not mo:
                raise UnableToParseDialogBackendVersion(s)
            dotted_part = [ int(x) for x in mo.group("dotted").split(".") ]
            rest = mo.group("rest")
        except re.error as e:
            raise PythonDialogReModuleError(str(e)) from e

        return cls(dotted_part, rest)

    def __lt__(self, other):
        return (self.dotted_part, self.rest) < (other.dotted_part, other.rest)

    def __le__(self, other):
        return (self.dotted_part, self.rest) <= (other.dotted_part, other.rest)

    def __eq__(self, other):
        return (self.dotted_part, self.rest) == (other.dotted_part, other.rest)

    # Python 3.2 has a decorator (functools.total_ordering) to automate this.
    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)


def widget(func):
    """Decorator to mark :class:`Dialog` methods that provide widgets.

    This allows code to perform automatic operations on these specific
    methods. For instance, one can define a class that behaves similarly
    to :class:`Dialog`, except that after every widget-producing call,
    it spawns a "confirm quit" dialog if the widget returned
    :attr:`Dialog.ESC`, and loops in case the user doesn't actually want
    to quit.

    When it is unclear whether a method should have the decorator or
    not, the return value is used to draw the line. For instance, among
    :meth:`Dialog.gauge_start`, :meth:`Dialog.gauge_update` and
    :meth:`Dialog.gauge_stop`, only the last one has the decorator
    because it returns a :term:`Dialog exit code`, whereas the first two
    don't return anything meaningful.

    Note:

      Some widget-producing methods return the Dialog exit code, but
      other methods return a *sequence*, the first element of which is
      the Dialog exit code; the ``retval_is_code`` attribute, which is
      set by the decorator of the same name, allows to programmatically
      discover the interface a given method conforms to.

    .. versionadded:: 2.14

    """
    func.is_widget = True
    return func


def retval_is_code(func):
    """Decorator for :class:`Dialog` widget-producing methods whose \
return value is the :term:`Dialog exit code`.

    This decorator is intended for widget-producing methods whose return
    value consists solely of the Dialog exit code. When this decorator
    is *not* used on a widget-producing method, the Dialog exit code
    must be the first element of the return value.

    .. versionadded:: 3.0

    """
    func.retval_is_code = True
    return func


def _obsolete_property(name, replacement=None):
    if replacement is None:
        replacement = name

    def getter(self):
        warnings.warn("the DIALOG_{name} attribute of Dialog instances is "
                      "obsolete; use the Dialog.{repl} class attribute "
                      "instead.".format(name=name, repl=replacement),
                      DeprecationWarning)
        return getattr(self, replacement)

    return getter


# Main class of the module
class Dialog:
    """Class providing bindings for :program:`dialog`-compatible programs.

    This class allows you to invoke :program:`dialog` or a compatible
    program in a pythonic way to quickly and easily build simple but
    nice text interfaces.

    An application typically creates one instance of the :class:`Dialog`
    class and uses it for all its widgets, but it is possible to
    concurrently use several instances of this class with different
    parameters (such as the background title) if you have a need for
    this.

    """
    try:
        _print_maxsize_cre = re.compile(r"""^MaxSize:[ \t]+
                                            (?P<rows>\d+),[ \t]*
                                            (?P<columns>\d+)[ \t]*$""",
                                        re.VERBOSE)
        _print_version_cre = re.compile(
            r"^Version:[ \t]+(?P<version>.+?)[ \t]*$", re.MULTILINE)
    except re.error as e:
        raise PythonDialogReModuleError(str(e)) from e

    # DIALOG_OK, DIALOG_CANCEL, etc. are environment variables controlling
    # the dialog backend exit status in the corresponding situation ("low-level
    # exit status/code").
    #
    # Note:
    #    - 127 must not be used for any of the DIALOG_* values. It is used
    #      when a failure occurs in the child process before it exec()s
    #      dialog (where "before" includes a potential exec() failure).
    #    - 126 is also used (although in presumably rare situations).
    _DIALOG_OK        = 0
    _DIALOG_CANCEL    = 1
    _DIALOG_ESC       = 2
    _DIALOG_ERROR     = 3
    _DIALOG_EXTRA     = 4
    _DIALOG_HELP      = 5
    _DIALOG_ITEM_HELP = 6
    # cf. also _lowlevel_exit_codes and _dialog_exit_code_ll_to_hl which are
    # created by __init__(). It is not practical to define everything here,
    # because there is no equivalent of 'self' for the class outside method
    # definitions.
    _lowlevel_exit_code_varnames = frozenset(("OK", "CANCEL", "ESC", "ERROR",
                                              "EXTRA", "HELP", "ITEM_HELP"))

    # High-level exit codes, AKA "Dialog exit codes". These are the codes that
    # pythondialog-based applications should use.
    #
    #: :term:`Dialog exit code` corresponding to the ``DIALOG_OK``
    #: :term:`dialog exit status`
    OK     = "ok"
    #: :term:`Dialog exit code` corresponding to the ``DIALOG_CANCEL``
    #: :term:`dialog exit status`
    CANCEL = "cancel"
    #: :term:`Dialog exit code` corresponding to the ``DIALOG_ESC``
    #: :term:`dialog exit status`
    ESC    = "esc"
    #: :term:`Dialog exit code` corresponding to the ``DIALOG_EXTRA``
    #: :term:`dialog exit status`
    EXTRA  = "extra"
    #: :term:`Dialog exit code` corresponding to the ``DIALOG_HELP`` and
    #: ``DIALOG_ITEM_HELP`` :term:`dialog exit statuses <dialog exit status>`
    HELP   = "help"

    # Define properties to maintain backward-compatibility while warning about
    # the obsolete attributes (which used to refer to the low-level exit codes
    # in pythondialog 2.x).
    #
    #: Obsolete property superseded by :attr:`Dialog.OK` since version 3.0
    DIALOG_OK        = property(_obsolete_property("OK"),
                         doc="Obsolete property superseded by Dialog.OK")
    #: Obsolete property superseded by :attr:`Dialog.CANCEL` since version 3.0
    DIALOG_CANCEL    = property(_obsolete_property("CANCEL"),
                         doc="Obsolete property superseded by Dialog.CANCEL")
    #: Obsolete property superseded by :attr:`Dialog.ESC` since version 3.0
    DIALOG_ESC       = property(_obsolete_property("ESC"),
                         doc="Obsolete property superseded by Dialog.ESC")
    #: Obsolete property superseded by :attr:`Dialog.EXTRA` since version 3.0
    DIALOG_EXTRA     = property(_obsolete_property("EXTRA"),
                         doc="Obsolete property superseded by Dialog.EXTRA")
    #: Obsolete property superseded by :attr:`Dialog.HELP` since version 3.0
    DIALOG_HELP      = property(_obsolete_property("HELP"),
                         doc="Obsolete property superseded by Dialog.HELP")
    # We treat DIALOG_ITEM_HELP and DIALOG_HELP the same way in pythondialog,
    # since both indicate the same user action ("Help" button pressed).
    #
    #: Obsolete property superseded by :attr:`Dialog.HELP` since version 3.0
    DIALOG_ITEM_HELP = property(_obsolete_property("ITEM_HELP",
                                                   replacement="HELP"),
                         doc="Obsolete property superseded by Dialog.HELP")

    @property
    def DIALOG_ERROR(self):
        warnings.warn("the DIALOG_ERROR attribute of Dialog instances is "
                      "obsolete. Since the corresponding exit status is "
                      "automatically translated into a DialogError exception, "
                      "users should not see nor need this attribute. If you "
                      "think you have a good reason to use it, please expose "
                      "your situation on the pythondialog mailing-list.",
                      DeprecationWarning)
        # There is no corresponding high-level code; and if the user *really*
        # wants to know the (integer) error exit status, here it is...
        return self._DIALOG_ERROR

    def __init__(self, dialog="dialog", DIALOGRC=None,
                 compat="dialog", use_stdout=None, *, autowidgetsize=False,
                 pass_args_via_file=None):
        """Constructor for :class:`Dialog` instances.

        :param str dialog:
          name of (or path to) the :program:`dialog`-like program to
          use. If it contains a slash (``/``), it must be a relative or
          absolute path to a file that has read and execute permissions,
          and is used as is; otherwise, it is looked for according to
          the contents of the :envvar:`PATH` environment variable, which
          defaults to ``/bin:/usr/bin`` if unset. In case you decide to
          use a relative path containing a ``/``, be *very careful*
          about the current directory at the time the Dialog instance is
          created. Indeed, if for instance you use ``"foobar/dialog"``
          and your program creates the Dialog instance at a time where
          the current directory is for instance ``/tmp``, then
          ``/tmp/foobar/dialog`` will be run, which could be risky. If
          you don't understand this, stay with the default, use a value
          containing no ``/``, or use an absolute path (i.e., one
          starting with a ``/``).
        :param str DIALOGRC:
          string to pass to the :program:`dialog`-like program as the
          :envvar:`DIALOGRC` environment variable, or ``None`` if no
          modification to the environment regarding this variable should
          be done in the call to the :program:`dialog`-like program
        :param str compat:
          compatibility mode (see :ref:`below
          <Dialog-constructor-compat-arg>`)
        :param bool use_stdout:
          read :program:`dialog`'s standard output stream instead of its
          standard error stream in order to get most "results"
          (user-supplied strings, selected items, etc.; basically,
          everything except the exit status). This is for compatibility
          with :program:`Xdialog` and should only be used if you have a
          good reason to do so.
        :param bool autowidgetsize:
          whether to enable *autowidgetsize* mode. When enabled, all
          pythondialog widget-producing methods will behave as if
          ``width=0``, ``height=0``, etc. had been passed, except where
          these parameters are explicitely specified with different
          values. This has the effect that, by default, the
          :program:`dialog` backend will automatically compute a
          suitable size for the widgets. More details about this option
          are given :ref:`below <autowidgetsize>`.
        :param pass_args_via_file:
          whether to use the :option:`--file` option with a temporary
          file in order to pass arguments to the :program:`dialog`
          backend, instead of including them directly into the argument
          list; using :option:`--file` has the advantage of not exposing
          the “real” arguments to other users through the process table.
          With the default value (``None``), the option is enabled if
          the :program:`dialog` version is recent enough to offer a
          reliable :option:`--file` implementation (i.e., 1.2-20150513
          or later).
        :type pass_args_via_file: bool or ``None``
        :return: a :class:`Dialog` instance

        .. _Dialog-constructor-compat-arg:

        The officially supported :program:`dialog`-like program in
        pythondialog is the well-known dialog_ program written in C,
        based on the ncurses_ library.

        .. _dialog: https://invisible-island.net/dialog/dialog.html
        .. _ncurses: https://invisible-island.net/ncurses/ncurses.html

        If you want to use a different program such as Xdialog_, you
        should indicate the executable file name with the *dialog*
        argument **and** the compatibility type that you think it
        conforms to with the *compat* argument. Currently, *compat* can
        be either ``"dialog"`` (for :program:`dialog`; this is the
        default) or ``"Xdialog"`` (for, well, :program:`Xdialog`).

        .. _Xdialog: http://xdialog.free.fr/

        The *compat* argument allows me to cope with minor differences
        in behaviour between the various programs implementing the
        :program:`dialog` interface (not the text or graphical
        interface, I mean the API). However, having to support various
        APIs simultaneously is ugly and I would really prefer you to
        report bugs to the relevant maintainers when you find
        incompatibilities with :program:`dialog`. This is for the
        benefit of pretty much everyone that relies on the
        :program:`dialog` interface.

        Notable exceptions:

          - :exc:`ExecutableNotFound`
          - :exc:`PythonDialogOSError`
          - :exc:`UnableToRetrieveBackendVersion`
          - :exc:`UnableToParseBackendVersion`

        .. versionadded:: 3.1
           Support for the *autowidgetsize* parameter.

        .. versionadded:: 3.3
           Support for the *pass_args_via_file* parameter.

        """
        # DIALOGRC differs from the Dialog._DIALOG_* attributes in that:
        #   1. It is an instance attribute instead of a class attribute.
        #   2. It should be a string if not None.
        #   3. We may very well want it to be unset.
        if DIALOGRC is not None:
            self.DIALOGRC = DIALOGRC

        # Mapping from "OK", "CANCEL", ... to the corresponding dialog exit
        # statuses (integers).
        self._lowlevel_exit_codes = {
            name: getattr(self, "_DIALOG_" + name)
            for name in self._lowlevel_exit_code_varnames }

        # Mapping from dialog exit status (integer) to Dialog exit code ("ok",
        # "cancel", ... strings referred to by Dialog.OK, Dialog.CANCEL, ...);
        # in other words, from low-level to high-level exit code.
        self._dialog_exit_code_ll_to_hl = {}
        for name in self._lowlevel_exit_code_varnames:
            intcode = self._lowlevel_exit_codes[name]

            if name == "ITEM_HELP":
                self._dialog_exit_code_ll_to_hl[intcode] = self.HELP
            elif name == "ERROR":
                continue
            else:
                self._dialog_exit_code_ll_to_hl[intcode] = getattr(self, name)

        self._dialog_prg = _path_to_executable(dialog)
        self.compat = compat
        self.autowidgetsize = autowidgetsize
        self.dialog_persistent_arglist = []

        # Use stderr or stdout for reading dialog's output?
        if self.compat == "Xdialog":
            # Default to using stdout for Xdialog
            self.use_stdout = True
        else:
            self.use_stdout = False
        if use_stdout is not None:
            # Allow explicit setting
            self.use_stdout = use_stdout
        if self.use_stdout:
            self.add_persistent_args(["--stdout"])

        self.setup_debug(False)

        if compat == "dialog":
            # Temporary setting to ensure that self.backend_version()
            # will be able to run even if dialog is too old to support
            # --file correctly. Will be overwritten later.
            self.pass_args_via_file = False
            self.cached_backend_version = DialogBackendVersion.fromstring(
                self.backend_version())
        else:
            # Xdialog doesn't seem to offer --print-version (2013-09-12)
            self.cached_backend_version = None

        if pass_args_via_file is not None:
            # Always respect explicit settings
            self.pass_args_via_file = pass_args_via_file
        elif self.cached_backend_version is not None:
            self.pass_args_via_file = self.cached_backend_version >= \
                                      DialogBackendVersion("1.2-20150513")
        else:
            # Xdialog doesn't seem to offer --file (2015-05-24)
            self.pass_args_via_file = False

    @classmethod
    def dash_escape(cls, args):
        """
        Escape all elements of *args* that need escaping for :program:`dialog`.

        *args* may be any sequence and is not modified by this method.
        Return a new list where every element that needs escaping has
        been escaped.

        An element needs escaping when it starts with two ASCII hyphens
        (``--``). Escaping consists in prepending an element composed of
        two ASCII hyphens, i.e., the string ``'--'``.

        All high-level :class:`Dialog` methods automatically perform
        :term:`dash escaping` where appropriate. In particular, this is
        the case for every method that provides a widget: :meth:`yesno`,
        :meth:`msgbox`, etc. You only need to do it yourself when
        calling a low-level method such as :meth:`add_persistent_args`.

        .. versionadded:: 2.12

        """
        return _dash_escape(args)

    @classmethod
    def dash_escape_nf(cls, args):
        """
        Escape all elements of *args* that need escaping, except the first one.

        See :meth:`dash_escape` for details. Return a new list.

        All high-level :class:`Dialog` methods automatically perform dash
        escaping where appropriate. In particular, this is the case
        for every method that provides a widget: :meth:`yesno`, :meth:`msgbox`,
        etc. You only need to do it yourself when calling a low-level
        method such as :meth:`add_persistent_args`.

        .. versionadded:: 2.12

        """
        return _dash_escape_nf(args)

    def add_persistent_args(self, args):
        """Add arguments to use for every subsequent dialog call.

        This method cannot guess which elements of *args* are dialog
        options (such as ``--title``) and which are not (for instance,
        you might want to use ``--title`` or even ``--`` as an argument
        to a dialog option). Therefore, this method does not perform any
        kind of :term:`dash escaping`; you have to do it yourself.
        :meth:`dash_escape` and :meth:`dash_escape_nf` may be useful for
        this purpose.

        """
        self.dialog_persistent_arglist.extend(args)

    def set_background_title(self, text):
        """Set the background title for dialog.

        :param str text: string to use as background title

        .. versionadded:: 2.13

        """
        self.add_persistent_args(self.dash_escape_nf(("--backtitle", text)))

    # For compatibility with the old dialog
    def setBackgroundTitle(self, text):
        """Set the background title for :program:`dialog`.

        :param str text: background title to use behind widgets

        .. deprecated:: 2.03
          Use :meth:`set_background_title` instead.

        """
        warnings.warn("Dialog.setBackgroundTitle() has been obsolete for "
                      "many years; use Dialog.set_background_title() instead",
                      DeprecationWarning)
        self.set_background_title(text)

    def setup_debug(self, enable, file=None, always_flush=False, *,
                    expand_file_opt=False):
        """Setup the debugging parameters.

        :param bool enable:       whether to enable or disable debugging
        :param file file:         where to write debugging information
        :param bool always_flush: whether to call :meth:`file.flush`
                                  after each command written
        :param bool expand_file_opt:
          when :meth:`Dialog.__init__` has been called with
          :samp:`{pass_args_via_file}=True`, this option causes the
          :option:`--file` options that would normally be written to
          *file* to be expanded, yielding a similar result to what would
          be obtained with :samp:`{pass_args_via_file}=False` (but
          contrary to :samp:`{pass_args_via_file}=False`, this only
          affects *file*, not the actual :program:`dialog` calls). This
          is useful, for instance, for copying some of the
          :program:`dialog` commands into a shell.

        When *enable* is true, all :program:`dialog` commands are
        written to *file* using POSIX shell syntax. In this case, you'll
        probably want to use either :samp:`{expand_file_opt}=True` in
        this method or :samp:`{pass_args_via_file}=False` in
        :meth:`Dialog.__init__`, otherwise you'll mostly see
        :program:`dialog` calls containing only one :option:`--file`
        option followed by a path to a temporary file.

        .. versionadded:: 2.12

        .. versionadded:: 3.3
           Support for the *expand_file_opt* parameter.

        """
        self._debug_enabled = enable

        if not hasattr(self, "_debug_logfile"):
            self._debug_logfile = None
        # Allows to switch debugging on and off without having to pass the file
        # object again and again.
        if file is not None:
            self._debug_logfile = file

        if enable and self._debug_logfile is None:
            raise BadPythonDialogUsage(
                "you must specify a file object when turning debugging on")

        self._debug_always_flush = always_flush
        self._expand_file_opt = expand_file_opt
        self._debug_first_output = True

    def _write_command_to_file(self, env, arglist):
        envvar_settings_list = []

        if "DIALOGRC" in env:
            envvar_settings_list.append(
                "DIALOGRC={0}".format(_shell_quote(env["DIALOGRC"])))

        for var in self._lowlevel_exit_code_varnames:
            varname = "DIALOG_" + var
            envvar_settings_list.append(
                "{0}={1}".format(varname, _shell_quote(env[varname])))

        command_str = ' '.join(envvar_settings_list +
                               list(map(_shell_quote, arglist)))
        s = "{separator}{cmd}\n\nArgs: {args!r}\n".format(
            separator="" if self._debug_first_output else ("-" * 79) + "\n",
            cmd=command_str, args=arglist)

        self._debug_logfile.write(s)
        if self._debug_always_flush:
            self._debug_logfile.flush()

        self._debug_first_output = False

    def _quote_arg_for_file_opt(self, argument):
        """
        Transform a :program:`dialog` argument for safe inclusion via :option:`--file`.

        Since arguments in a file included via :option:`--file` are
        separated by whitespace, they must be quoted for
        :program:`dialog` in a way similar to shell quoting.

        """
        l = ['"']

        for c in argument:
            if c in ('"', '\\'):
                l.append("\\" + c)
            else:
                l.append(c)

        return ''.join(l + ['"'])

    def _call_program(self, cmdargs, *, dash_escape="non-first",
                      use_persistent_args=True,
                      redir_child_stdin_from_fd=None, close_fds=(), **kwargs):
        """Do the actual work of invoking the :program:`dialog`-like program.

        Communication with the :program:`dialog`-like program is
        performed through one :manpage:`pipe(2)` and optionally a
        user-specified file descriptor, depending on
        *redir_child_stdin_from_fd*. The pipe allows the parent process
        to read what :program:`dialog` writes on its standard error
        stream [#]_.

        If *use_persistent_args* is ``True`` (the default), the elements
        of ``self.dialog_persistent_arglist`` are passed as the first
        arguments to ``self._dialog_prg``; otherwise,
        ``self.dialog_persistent_arglist`` is not used at all. The
        remaining arguments are those computed from *kwargs* followed by
        the elements of *cmdargs*.

        If *dash_escape* is the string ``"non-first"``, then every
        element of *cmdargs* that starts with ``'--'`` is escaped by
        prepending an element consisting of ``'--'``, except the first
        one (which is usually a :program:`dialog` option such as
        ``'--yesno'``). In order to disable this escaping mechanism,
        pass the string ``"none"`` as *dash_escape*.

        If *redir_child_stdin_from_fd* is not ``None``, it should be an
        open file descriptor (i.e., an integer). That file descriptor
        will be connected to :program:`dialog`'s standard input. This is
        used by the gauge widget to feed data to :program:`dialog`, as
        well as for :meth:`progressbox` in order to allow
        :program:`dialog` to read data from a possibly-growing file.

        If *redir_child_stdin_from_fd* is ``None``, the standard input
        in the child process (which runs :program:`dialog`) is not
        redirected in any way.

        If *close_fds* is passed, it should be a sequence of file
        descriptors that will be closed by the child process before it
        exec()s the :program:`dialog`-like program.

        Notable exception:

          :exc:`PythonDialogOSError` (if any of the pipe(2) or close(2)
          system calls fails...)

        .. [#] standard ouput stream if *use_stdout* is ``True``

        """
        # We want to define DIALOG_OK, DIALOG_CANCEL, etc. in the
        # environment of the child process so that we know (and
        # even control) the possible dialog exit statuses.
        new_environ = {}
        new_environ.update(os.environ)
        for var, value in self._lowlevel_exit_codes.items():
            varname = "DIALOG_" + var
            new_environ[varname] = str(value)
        if hasattr(self, "DIALOGRC"):
            new_environ["DIALOGRC"] = self.DIALOGRC

        if dash_escape == "non-first":
            # Escape all elements of 'cmdargs' that start with '--', except the
            # first one.
            cmdargs = self.dash_escape_nf(cmdargs)
        elif dash_escape != "none":
            raise PythonDialogBug("invalid value for 'dash_escape' parameter: "
                                  "{0!r}".format(dash_escape))

        arglist = [ self._dialog_prg ]

        if use_persistent_args:
            arglist.extend(self.dialog_persistent_arglist)

        arglist.extend(_compute_common_args(kwargs) + cmdargs)
        orig_args = arglist[:] # New object, copy of 'arglist'

        if self.pass_args_via_file:
            tmpfile = tempfile.NamedTemporaryFile(
                mode="w", prefix="pythondialog.tmp", delete=False)
            with tmpfile as f:
                f.write(' '.join( ( self._quote_arg_for_file_opt(arg)
                                    for arg in arglist[1:] ) ))
            args_file = tmpfile.name
            arglist[1:] = ["--file", args_file]
        else:
            args_file = None

        if self._debug_enabled:
            # Write the complete command line with environment variables
            # setting to the debug log file (POSIX shell syntax for easy
            # copy-pasting into a terminal, followed by repr(arglist)).
            self._write_command_to_file(
                new_environ, orig_args if self._expand_file_opt else arglist)

        # Create a pipe so that the parent process can read dialog's
        # output on stderr (stdout with 'use_stdout')
        with _OSErrorHandling():
            # rfd = File Descriptor for Reading
            # wfd = File Descriptor for Writing
            (child_output_rfd, child_output_wfd) = os.pipe()

        child_pid = os.fork()
        if child_pid == 0:
            # We are in the child process. We MUST NOT raise any exception.
            try:
                # 1) If the write end of a pipe isn't closed, the read end
                #    will never see EOF, which can indefinitely block the
                #    child waiting for input. To avoid this, the write end
                #    must be closed in the father *and* child processes.
                # 2) The child process doesn't need child_output_rfd.
                for fd in close_fds + (child_output_rfd,):
                    os.close(fd)
                # We want:
                #   - to keep a reference to the father's stderr for error
                #     reporting (and use line-buffering for this stream);
                #   - dialog's output on stderr[*] to go to child_output_wfd;
                #   - data written to fd 'redir_child_stdin_from_fd'
                #     (if not None) to go to dialog's stdin.
                #
                #       [*] stdout with 'use_stdout'
                father_stderr = os.fdopen(os.dup(2), mode="w", buffering=1)
                os.dup2(child_output_wfd, 1 if self.use_stdout else 2)
                if redir_child_stdin_from_fd is not None:
                    os.dup2(redir_child_stdin_from_fd, 0)

                os.execve(self._dialog_prg, arglist, new_environ)
            except:
                print(traceback.format_exc(), file=father_stderr)
                father_stderr.close()
                os._exit(127)

            # Should not happen unless there is a bug in Python
            os._exit(126)

        # We are in the father process.
        #
        # It is essential to close child_output_wfd, otherwise we will never
        # see EOF while reading on child_output_rfd and the parent process
        # will block forever on the read() call.
        # [ after the fork(), the "reference count" of child_output_wfd from
        #   the operating system's point of view is 2; after the child exits,
        #   it is 1 until the father closes it itself; then it is 0 and a read
        #   on child_output_rfd encounters EOF once all the remaining data in
        #   the pipe has been read. ]
        with _OSErrorHandling():
            os.close(child_output_wfd)
        return (child_pid, child_output_rfd, args_file)

    def _wait_for_program_termination(self, child_pid, child_output_rfd):
        """Wait for a :program:`dialog`-like process to terminate.

        This function waits for the specified process to terminate,
        raises the appropriate exceptions in case of abnormal
        termination and returns the :term:`Dialog exit code` and stderr
        [#stream]_ output of the process as a tuple: :samp:`({hl_exit_code},
        {output_string})`.

        *child_output_rfd* must be the file descriptor for the
        reading end of the pipe created by :meth:`_call_program`, the
        writing end of which was connected by :meth:`_call_program`
        to the child process's standard error [#stream]_.

        This function reads the process output on the standard error
        [#stream]_ from *child_output_rfd* and closes this file
        descriptor once this is done.

        Notable exceptions:

          - :exc:`DialogTerminatedBySignal`
          - :exc:`DialogError`
          - :exc:`PythonDialogErrorBeforeExecInChildProcess`
          - :exc:`PythonDialogIOError`    if the Python version is < 3.3
          - :exc:`PythonDialogOSError`
          - :exc:`PythonDialogBug`
          - :exc:`ProbablyPythonBug`

        .. [#stream] standard output if ``self.use_stdout`` is ``True``

        """
        # Read dialog's output on its stderr (stdout with 'use_stdout')
        with _OSErrorHandling():
            with os.fdopen(child_output_rfd, "r") as f:
                child_output = f.read()
            # The closing of the file object causes the end of the pipe we used
            # to read dialog's output on its stderr to be closed too. This is
            # important, otherwise invoking dialog enough times would
            # eventually exhaust the maximum number of open file descriptors.

        exit_info = os.waitpid(child_pid, 0)[1]
        if os.WIFEXITED(exit_info):
            ll_exit_code = os.WEXITSTATUS(exit_info)
        # As we wait()ed for the child process to terminate, there is no
        # need to call os.WIFSTOPPED()
        elif os.WIFSIGNALED(exit_info):
            raise DialogTerminatedBySignal("the dialog-like program was "
                                           "terminated by signal %d" %
                                           os.WTERMSIG(exit_info))
        else:
            raise PythonDialogBug("please report this bug to the "
                                  "pythondialog maintainer(s)")

        if ll_exit_code == self._DIALOG_ERROR:
            raise DialogError(
                "the dialog-like program exited with status {0} (which was "
                "passed to it as the DIALOG_ERROR environment variable). "
                "Sometimes, the reason is simply that dialog was given a "
                "height or width parameter that is too big for the terminal "
                "in use. Its output, with leading and trailing whitespace "
                "stripped, was:\n\n{1}".format(ll_exit_code,
                                               child_output.strip()))
        elif ll_exit_code == 127:
            raise PythonDialogErrorBeforeExecInChildProcess(dedent("""\
            possible reasons include:
              - the dialog-like program could not be executed (this can happen
                for instance if the Python program is trying to call the
                dialog-like program with arguments that cannot be represented
                in the user's locale [LC_CTYPE]);
              - the system is out of memory;
              - the maximum number of open file descriptors has been reached;
              - a cosmic ray hit the system memory and flipped nasty bits.
            There ought to be a traceback above this message that describes
            more precisely what happened."""))
        elif ll_exit_code == 126:
            raise ProbablyPythonBug(
                "a child process returned with exit status 126; this might "
                "be the exit status of the dialog-like program, for some "
                "unknown reason (-> probably a bug in the dialog-like "
                "program); otherwise, we have probably found a python bug")

        try:
            hl_exit_code = self._dialog_exit_code_ll_to_hl[ll_exit_code]
        except KeyError:
            raise PythonDialogBug(
                "unexpected low-level exit status (new code?): {0!r}".format(
                    ll_exit_code))

        return (hl_exit_code, child_output)

    def _handle_program_exit(self, child_pid, child_output_rfd, args_file):
        """Handle exit of a :program:`dialog`-like process.

        This method:

          - waits for the :program:`dialog`-like program termination;
          - removes the temporary file used to pass its argument list,
            if any;
          - and returns the appropriate :term:`Dialog exit code` along
            with whatever output it produced.

        Notable exceptions:

          any exception raised by :meth:`_wait_for_program_termination`

        """
        try:
            exit_code, output = \
                    self._wait_for_program_termination(child_pid,
                                                       child_output_rfd)
        finally:
            with _OSErrorHandling():
                if args_file is not None and os.path.exists(args_file):
                    os.unlink(args_file)

        return (exit_code, output)

    def _perform(self, cmdargs, *, dash_escape="non-first",
                 use_persistent_args=True, **kwargs):
        """Perform a complete :program:`dialog`-like program invocation.

        This method:

          - invokes the :program:`dialog`-like program;
          - waits for its termination;
          - removes the temporary file used to pass its argument list,
            if any;
          - and returns the appropriate :term:`Dialog exit code` along
            with whatever output it produced.

        See :meth:`_call_program` for a description of the parameters.

        Notable exceptions:

          any exception raised by :meth:`_call_program` or
          :meth:`_handle_program_exit`

        """
        child_pid, child_output_rfd, args_file = \
                    self._call_program(cmdargs, dash_escape=dash_escape,
                                       use_persistent_args=use_persistent_args,
                                       **kwargs)
        exit_code, output = self._handle_program_exit(child_pid,
                                                      child_output_rfd,
                                                      args_file)

        return (exit_code, output)

    def _strip_xdialog_newline(self, output):
        """Remove trailing newline (if any) in \
:program:`Xdialog`-compatibility mode"""
        if self.compat == "Xdialog" and output.endswith("\n"):
            output = output[:-1]
        return output

    # This is for compatibility with the old dialog.py
    def _perform_no_options(self, cmd):
        """Call :program:`dialog` without passing any more options."""

        warnings.warn("Dialog._perform_no_options() has been obsolete for "
                      "many years", DeprecationWarning)
        return os.system(self._dialog_prg + ' ' + cmd)

    # For compatibility with the old dialog.py
    def clear(self):
        """Clear the screen.

        Equivalent to the :option:`--clear` option of :program:`dialog`.

        .. deprecated:: 2.03
          You may use the :manpage:`clear(1)` program instead.
          cf. ``clear_screen()`` in :file:`examples/demo.py` for an
          example.

        """
        warnings.warn("Dialog.clear() has been obsolete for many years.\n"
                      "You may use the clear(1) program to clear the screen.\n"
                      "cf. clear_screen() in examples/demo.py for an example",
                      DeprecationWarning)
        self._perform_no_options('--clear')

    def _help_status_on(self, kwargs):
        return ("--help-status" in self.dialog_persistent_arglist
                or kwargs.get("help_status", False))

    def _parse_quoted_string(self, s, start=0):
        """Parse a quoted string from a :program:`dialog` help output."""
        if start >= len(s) or s[start] != '"':
            raise PythonDialogBug("quoted string does not start with a double "
                                  "quote: {0!r}".format(s))

        l = []
        i = start + 1

        while i < len(s) and s[i] != '"':
            if s[i] == "\\":
                i += 1
                if i >= len(s):
                    raise PythonDialogBug(
                        "quoted string ends with a backslash: {0!r}".format(s))
            l.append(s[i])
            i += 1

        if s[i] != '"':
            raise PythonDialogBug("quoted string does not and with a double "
                                  "quote: {0!r}".format(s))

        return (''.join(l), i+1)

    def _split_shellstyle_arglist(self, s):
        """Split an argument list with shell-style quoting performed \
by :program:`dialog`.

        Any argument in 's' may or may not be quoted. Quoted
        arguments are always expected to be enclosed in double quotes
        (more restrictive than what the POSIX shell allows).

        This function could maybe be replaced with shlex.split(),
        however:
          - shlex only handles Unicode strings in Python 2.7.3 and
            above;
          - the bulk of the work is done by _parse_quoted_string(),
            which is probably still needed in _parse_help(), where
            one needs to parse things such as 'HELP <id> <status>' in
            which <id> may be quoted but <status> is never quoted,
            even if it contains spaces or quotes.

        """
        s = s.rstrip()
        l = []
        i = 0

        while i < len(s):
            if s[i] == '"':
                arg, i = self._parse_quoted_string(s, start=i)
                if i < len(s) and s[i] != ' ':
                    raise PythonDialogBug(
                        "expected a space or end-of-string after quoted "
                        "string in {0!r}, but found {1!r}".format(s, s[i]))
                # Start of the next argument, or after the end of the string
                i += 1
                l.append(arg)
            else:
                try:
                    end = s.index(' ', i)
                except ValueError:
                    end = len(s)

                l.append(s[i:end])
                # Start of the next argument, or after the end of the string
                i = end + 1

        return l

    def _parse_help(self, output, kwargs, *, multival=False,
                    multival_on_single_line=False, raw_format=False):
        """Parse the dialog help output from a widget.

        'kwargs' should contain the keyword arguments used in the
        widget call that produced the help output.

        'multival' is for widgets that return a list of values as
        opposed to a single value.

        'raw_format' is for widgets that don't start their help
        output with the string "HELP ".

        """
        l = output.splitlines()

        if raw_format:
            # This format of the help output is either empty or consists of
            # only one line (possibly terminated with \n). It is
            # encountered with --calendar and --inputbox, among others.
            if len(l) > 1:
                raise PythonDialogBug("raw help feedback unexpected as "
                                      "multiline: {0!r}".format(output))
            elif len(l) == 0:
                return ""
            else:
                return l[0]

        # Simple widgets such as 'yesno' will fall in this case if they use
        # this method.
        if not l:
            return None

        # The widgets that actually use --help-status always have the first
        # help line indicating the active item; there is no risk of
        # confusing this line with the first line produced by --help-status.
        if not l[0].startswith("HELP "):
            raise PythonDialogBug(
                "unexpected help output that does not start with 'HELP ': "
                "{0!r}".format(output))

        # Everything that follows "HELP "; what it contains depends on whether
        # --item-help and/or --help-tags were passed to dialog.
        s = l[0][5:]

        if not self._help_status_on(kwargs):
            return s

        if multival:
            if multival_on_single_line:
                args = self._split_shellstyle_arglist(s)
                if not args:
                    raise PythonDialogBug(
                        "expected a non-empty space-separated list of "
                        "possibly-quoted strings in this help output: {0!r}"
                        .format(output))
                return (args[0], args[1:])
            else:
                return (s, l[1:])
        else:
            if not s:
                raise PythonDialogBug(
                    "unexpected help output whose first line is 'HELP '")
            elif s[0] != '"':
                l2 = s.split(' ', 1)
                if len(l2) == 1:
                    raise PythonDialogBug(
                        "expected 'HELP <id> <status>' in the help output, "
                        "but couldn't find any space after 'HELP '")
                else:
                    return tuple(l2)
            else:
                help_id, after_index = self._parse_quoted_string(s)
                if not s[after_index:].startswith(" "):
                    raise PythonDialogBug(
                        "expected 'HELP <quoted_id> <status>' in the help "
                        "output, but couldn't find any space after "
                        "'HELP <quoted_id>'")
                return (help_id, s[after_index+1:])

    def _widget_with_string_output(self, args, kwargs,
                                   strip_xdialog_newline=False,
                                   raw_help=False):
        """Generic implementation for a widget that produces a single string.

        The help output must be present regardless of whether
        --help-status was passed or not.

        """
        code, output = self._perform(args, **kwargs)

        if strip_xdialog_newline:
            output = self._strip_xdialog_newline(output)

        if code == self.HELP:
            # No check for --help-status
            help_data = self._parse_help(output, kwargs, raw_format=raw_help)
            return (code, help_data)
        else:
            return (code, output)

    def _widget_with_no_output(self, widget_name, args, kwargs):
        """Generic implementation for a widget that produces no output."""
        code, output = self._perform(args, **kwargs)

        if output:
            raise PythonDialogBug(
                "expected an empty output from {0!r}, but got: {1!r}".format(
                    widget_name, output))

        return code

    def _dialog_version_check(self, version_string, feature):
        if self.compat == "dialog":
            minimum_version = DialogBackendVersion.fromstring(version_string)

            if self.cached_backend_version < minimum_version:
                raise InadequateBackendVersion(
                    "{0} requires dialog {1} or later, "
                    "but you seem to be using version {2}".format(
                        feature, minimum_version, self.cached_backend_version))

    def backend_version(self):
        """Get the version of the :program:`dialog`-like program (backend).

        If the version of the :program:`dialog`-like program can be
        retrieved, return it as a string; otherwise, raise
        :exc:`UnableToRetrieveBackendVersion`.

        This version is not to be confused with the pythondialog
        version.

        In most cases, you should rather use the
        :attr:`cached_backend_version` attribute of :class:`Dialog`
        instances, because:

          - it avoids calling the backend every time one needs the
            version;
          - it is a :class:`BackendVersion` instance (or instance of a
            subclass) that allows easy and reliable comparisons between
            versions;
          - the version string corresponding to a
            :class:`BackendVersion` instance (or instance of a subclass)
            can be obtained with :func:`str`.

        Notable exceptions:

          - :exc:`UnableToRetrieveBackendVersion`
          - :exc:`PythonDialogReModuleError`
          - any exception raised by :meth:`Dialog._perform`

        .. versionadded:: 2.12

        .. versionchanged:: 2.14
           Raise :exc:`UnableToRetrieveBackendVersion` instead of
           returning ``None`` when the version of the
           :program:`dialog`-like program can't be retrieved.

        """
        code, output = self._perform(["--print-version"],
                                     use_persistent_args=False)

        # Workaround for old dialog versions
        if code == self.OK and not (output.strip() or self.use_stdout):
            # output.strip() is empty and self.use_stdout is False.
            # This can happen with old dialog versions (1.1-20100428
            # apparently does that). Try again, reading from stdout this
            # time.
            self.use_stdout = True
            code, output = self._perform(["--stdout", "--print-version"],
                                         use_persistent_args=False,
                                         dash_escape="none")
            self.use_stdout = False

        if code == self.OK:
            try:
                mo = self._print_version_cre.match(output)
                if mo:
                    return mo.group("version")
                else:
                    raise UnableToRetrieveBackendVersion(
                        "unable to parse the output of '{0} --print-version': "
                        "{1!r}".format(self._dialog_prg, output))
            except re.error as e:
                raise PythonDialogReModuleError(str(e)) from e
        else:
            raise UnableToRetrieveBackendVersion(
                "exit code {0!r} from the backend".format(code))

    def maxsize(self, **kwargs):
        """Get the maximum size of dialog boxes.

        If the exit status from the backend corresponds to
        :attr:`Dialog.OK`, return a :samp:`({lines}, {cols})` tuple of
        integers; otherwise, return ``None``.

        If you want to obtain the number of lines and columns of the
        terminal, you should call this method with
        ``use_persistent_args=False``, because :program:`dialog` options
        such as :option:`--backtitle` modify the returned values.

        Notable exceptions:

          - :exc:`PythonDialogReModuleError`
          - any exception raised by :meth:`Dialog._perform`

        .. versionadded:: 2.12

        """
        code, output = self._perform(["--print-maxsize"], **kwargs)
        if code == self.OK:
            try:
                mo = self._print_maxsize_cre.match(output)
                if mo:
                    return tuple(map(int, mo.group("rows", "columns")))
                else:
                    raise PythonDialogBug(
                        "Unable to parse the output of '{0} --print-maxsize': "
                        "{1!r}".format(self._dialog_prg, output))
            except re.error as e:
                raise PythonDialogReModuleError(str(e)) from e
        else:
            return None

    def _default_size(self, values, defaults):
        # If 'autowidgetsize' is enabled, set the default values for the
        # width/height/... parameters of widget-producing methods to 0 (this
        # will actually be done by the caller, this function is only a helper).
        if self.autowidgetsize:
            defaults = (0,) * len(defaults)

        # For every element of 'values': keep it if different from None,
        # otherwise replace it with the corresponding value from 'defaults'.
        return [ v if v is not None else defaults[i]
                 for i, v in enumerate(values) ]

    @widget
    def buildlist(self, text, height=0, width=0, list_height=0, items=[],
                  **kwargs):
        """Display a buildlist box.

        :param str text:        text to display in the box
        :param int height:      height of the box
        :param int width:       width of the box
        :param int list_height: height of the selected and unselected
                                list boxes
        :param items:
          an iterable of :samp:`({tag}, {item}, {status})` tuples where
          *status* specifies the initial selected/unselected state of
          each entry; can be ``True`` or ``False``, ``1`` or ``0``,
          ``"on"`` or ``"off"`` (``True``, ``1`` and ``"on"`` meaning
          selected), or any case variation of these two strings.

        :return: a tuple of the form :samp:`({code}, {tags})` where:

          - *code* is a :term:`Dialog exit code`;
          - *tags* is a list of the tags corresponding to the selected
            items, in the order they have in the list on the right.

        :rtype: tuple

        A :meth:`!buildlist` dialog is similar in logic to the
        :meth:`checklist`, but differs in presentation. In this widget,
        two lists are displayed, side by side. The list on the left
        shows unselected items. The list on the right shows selected
        items. As items are selected or unselected, they move between
        the two lists. The *status* component of *items* specifies which
        items are initially selected.

        +--------------+------------------------------------------------+
        |     Key      |                     Action                     |
        +==============+================================================+
        | :kbd:`Space` | select or deselect the highlighted item,       |
        |              | *i.e.*, move it between the left and right     |
        |              | lists                                          |
        +--------------+------------------------------------------------+
        | :kbd:`^`     | move the focus to the left list                |
        +--------------+------------------------------------------------+
        | :kbd:`$`     | move the focus to the right list               |
        +--------------+------------------------------------------------+
        | :kbd:`Tab`   | move focus (see *visit_items* below)           |
        +--------------+------------------------------------------------+
        | :kbd:`Enter` | press the focused button                       |
        +--------------+------------------------------------------------+

        If called with ``visit_items=True``, the :kbd:`Tab` key can move
        the focus to the left and right lists, which is probably more
        intuitive for users than the default behavior that requires
        using :kbd:`^` and :kbd:`$` for this purpose.

        This widget requires dialog >= 1.2-20121230.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform` or :func:`_to_onoff`

        .. versionadded:: 3.0

        """
        self._dialog_version_check("1.2-20121230", "the buildlist widget")

        cmd = ["--buildlist", text, str(height), str(width), str(list_height)]
        for t in items:
            cmd.extend([ t[0], t[1], _to_onoff(t[2]) ] + list(t[3:]))

        code, output = self._perform(cmd, **kwargs)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs, multival=True,
                                         multival_on_single_line=True)
            if self._help_status_on(kwargs):
                help_id, selected_tags = help_data
                items = [ [ tag, item, tag in selected_tags ] + rest
                            for (tag, item, status, *rest) in items ]
                return (code, (help_id, selected_tags, items))
            else:
                return (code, help_data)
        elif code in (self.OK, self.EXTRA):
            return (code, self._split_shellstyle_arglist(output))
        else:
            return (code, None)

    def _calendar_parse_date(self, date_str):
        try:
            mo = _calendar_date_cre.match(date_str)
        except re.error as e:
            raise PythonDialogReModuleError(str(e)) from e

        if not mo:
            raise UnexpectedDialogOutput(
                "the dialog-like program returned the following "
                "unexpected output (a date string was expected) from the "
                "calendar box: {0!r}".format(date_str))

        return [ int(s) for s in mo.group("day", "month", "year") ]

    @widget
    def calendar(self, text, height=None, width=0, day=-1, month=-1, year=-1,
                 **kwargs):
        """Display a calendar dialog box.

        :param str text:  text to display in the box
        :param height:    height of the box (minus the calendar height)
        :type height:     int or ``None``
        :param int width: width of the box
        :param int day:   inititial day highlighted
        :param int month: inititial month displayed
        :param int year:  inititial year selected
        :return: a tuple of the form :samp:`({code}, {date})` where:

          - *code* is a :term:`Dialog exit code`;
          - *date* is a list of the form :samp:`[{day}, {month},
            {year}]`, where *day*, *month* and *year* are integers
            corresponding to the date chosen by the user.

        :rtype: tuple

        A :meth:`!calendar` box displays day, month and year in
        separately adjustable windows. If *year* is given as ``0``, the
        current date is used as initial value; otherwise, if any of the
        values for *day*, *month* and *year* is negative, the current
        date's corresponding value is used. You can increment or
        decrement any of those using the :kbd:`Left`, :kbd:`Up`,
        :kbd:`Right` and :kbd:`Down` arrows. Use :kbd:`Tab` or
        :kbd:`Backtab` to move between windows.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=6, width=0``.

        Notable exceptions:

          - any exception raised by :meth:`Dialog._perform`
          - :exc:`UnexpectedDialogOutput`
          - :exc:`PythonDialogReModuleError`

        .. versionchanged:: 3.2
           The default values for *day*, *month* and *year* have been
           changed from ``0`` to ``-1``.

        """
        (height,) = self._default_size((height, ), (6,))
        (code, output) = self._perform(
            ["--calendar", text, str(height), str(width), str(day),
               str(month), str(year)],
            **kwargs)

        if code == self.HELP:
            # The output does not depend on whether --help-status was passed
            # (dialog 1.2-20130902).
            help_data = self._parse_help(output, kwargs, raw_format=True)
            return (code, self._calendar_parse_date(help_data))
        elif code in (self.OK, self.EXTRA):
            return (code, self._calendar_parse_date(output))
        else:
            return (code, None)

    @widget
    def checklist(self, text, height=None, width=None, list_height=None,
                  choices=[], **kwargs):
        """Display a checklist box.

        :param str text:    text to display in the box
        :param height:      height of the box
        :type height:       int or ``None``
        :param width:       width of the box
        :type width:        int or ``None``
        :param list_height:
          number of entries displayed in the box at a given time (the
          contents can be scrolled)
        :type list_height:  int or ``None``
        :param choices:
          an iterable of :samp:`({tag}, {item}, {status})` tuples where
          *status* specifies the initial selected/unselected state of
          each entry; can be ``True`` or ``False``, ``1`` or ``0``,
          ``"on"`` or ``"off"`` (``True``, ``1`` and ``"on"`` meaning
          selected), or any case variation of these two strings.
        :return: a tuple of the form :samp:`({code}, [{tag}, ...])`
          whose first element is a :term:`Dialog exit code` and second
          element lists all tags for the entries selected by the user.
          If the user exits with :kbd:`Esc` or :guilabel:`Cancel`, the
          returned tag list is empty.

        :rtype: tuple

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=15, width=54, list_height=7``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform` or :func:`_to_onoff`

        """
        height, width, list_height = self._default_size(
            (height, width, list_height), (15, 54, 7))
        cmd = ["--checklist", text, str(height), str(width), str(list_height)]
        for t in choices:
            t = [ t[0], t[1], _to_onoff(t[2]) ] + list(t[3:])
            cmd.extend(t)

        # The dialog output cannot be parsed reliably (at least in dialog
        # 0.9b-20040301) without --separate-output (because double quotes in
        # tags are escaped with backslashes, but backslashes are not
        # themselves escaped and you have a problem when a tag ends with a
        # backslash--the output makes you think you've encountered an embedded
        # double-quote).
        kwargs["separate_output"] = True

        (code, output) = self._perform(cmd, **kwargs)
        # Since we used --separate-output, the tags are separated by a newline
        # in the output. There is also a final newline after the last tag.

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs, multival=True)
            if self._help_status_on(kwargs):
                help_id, selected_tags = help_data
                choices = [ [ tag, item, tag in selected_tags ] + rest
                            for (tag, item, status, *rest) in choices ]
                return (code, (help_id, selected_tags, choices))
            else:
                return (code, help_data)
        else:
            return (code, output.split('\n')[:-1])

    def _form_updated_items(self, status, elements):
        """Return a complete list with up-to-date items from 'status'.

        Return a new list of same length as 'elements'. Items are
        taken from 'status', except when data inside 'elements'
        indicates a read-only field: such items are not output by
        dialog ... --help-status ..., and therefore have to be
        extracted from 'elements' instead of 'status'.

        Actually, for 'mixedform', the elements that are defined as
        read-only using the attribute instead of a non-positive
        field_length are not concerned by this function, since they
        are included in the --help-status output.

        """
        res = []
        for i, (label, yl, xl, item, yi, xi, field_length, *rest) \
                in enumerate(elements):
            res.append(status[i] if field_length > 0 else item)

        return res

    def _generic_form(self, widget_name, method_name, text, elements, height=0,
                      width=0, form_height=0, **kwargs):
        cmd = ["--%s" % widget_name, text, str(height), str(width),
               str(form_height)]

        if not elements:
            raise BadPythonDialogUsage(
                "{0}.{1}.{2}: empty ELEMENTS sequence: {3!r}".format(
                    __name__, type(self).__name__, method_name, elements))

        elt_len = len(elements[0]) # for consistency checking
        for i, elt in enumerate(elements):
            if len(elt) != elt_len:
                raise BadPythonDialogUsage(
                    "{0}.{1}.{2}: ELEMENTS[0] has length {3}, whereas "
                    "ELEMENTS[{4}] has length {5}".format(
                        __name__, type(self).__name__, method_name,
                        elt_len, i, len(elt)))

            # Give names to make the code more readable
            if widget_name in ("form", "passwordform"):
                label, yl, xl, item, yi, xi, field_length, input_length = \
                    elt[:8]
                rest = elt[8:]  # optional "item_help" string
            elif widget_name == "mixedform":
                label, yl, xl, item, yi, xi, field_length, input_length, \
                    attributes = elt[:9]
                rest = elt[9:]  # optional "item_help" string
            else:
                raise PythonDialogBug(
                    "unexpected widget name in {0}.{1}._generic_form(): "
                    "{2!r}".format(__name__, type(self).__name__, widget_name))

            for name, value in (("label", label), ("item", item)):
                if not isinstance(value, str):
                    raise BadPythonDialogUsage(
                        "{0}.{1}.{2}: {3!r} element not a string: {4!r}".format(
                            __name__, type(self).__name__,
                            method_name, name, value))

            cmd.extend((label, str(yl), str(xl), item, str(yi), str(xi),
                        str(field_length), str(input_length)))
            if widget_name == "mixedform":
                cmd.append(str(attributes))
            # "item help" string when using --item-help, nothing otherwise
            cmd.extend(rest)

        (code, output) = self._perform(cmd, **kwargs)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs, multival=True)
            if self._help_status_on(kwargs):
                help_id, status = help_data
                # 'status' does not contain the fields marked as read-only in
                # 'elements'. Build a list containing all up-to-date items.
                updated_items = self._form_updated_items(status, elements)
                # Reconstruct 'elements' with the updated items taken from
                # 'status'.
                elements = [ [ label, yl, xl, updated_item ] + rest for
                             ((label, yl, xl, item, *rest), updated_item) in
                             zip(elements, updated_items) ]
                return (code, (help_id, status, elements))
            else:
                return (code, help_data)
        else:
            return (code, output.split('\n')[:-1])

    @widget
    def form(self, text, elements, height=0, width=0, form_height=0, **kwargs):
        """Display a form consisting of labels and fields.

        :param str text:        text to display in the box
        :param elements:        sequence describing the labels and
                                fields (see below)
        :param int height:      height of the box
        :param int width:       width of the box
        :param int form_height: number of form lines displayed at the
                                same time
        :return: a tuple of the form :samp:`({code}, {list})` where:

          - *code* is a :term:`Dialog exit code`;
          - *list* gives the contents of every editable field on exit,
            with the same order as in *elements*.

        :rtype: tuple

        A :meth:`!form` box consists in a series of :dfn:`fields` and
        associated :dfn:`labels`. This type of dialog is suitable for
        adjusting configuration parameters and similar tasks.

        Each element of *elements* must itself be a sequence
        :samp:`({label}, {yl}, {xl}, {item}, {yi}, {xi}, {field_length},
        {input_length})` containing the various parameters concerning a
        given field and the associated label.

        *label* is a string that will be displayed at row *yl*, column
        *xl*. *item* is a string giving the initial value for the field,
        which will be displayed at row *yi*, column *xi* (row and column
        numbers starting from 1).

        *field_length* and *input_length* are integers that respectively
        specify the number of characters used for displaying the field
        and the maximum number of characters that can be entered for
        this field. These two integers also determine whether the
        contents of the field can be modified, as follows:

          - if *field_length* is zero, the field cannot be altered and
            its contents determines the displayed length;

          - if *field_length* is negative, the field cannot be altered
            and the opposite of *field_length* gives the displayed
            length;

          - if *input_length* is zero, it is set to *field_length*.

        Notable exceptions:

          - :exc:`BadPythonDialogUsage`
          - any exception raised by :meth:`Dialog._perform`

        """
        return self._generic_form("form", "form", text, elements,
                                  height, width, form_height, **kwargs)

    @widget
    def passwordform(self, text, elements, height=0, width=0, form_height=0,
                     **kwargs):
        """Display a form consisting of labels and invisible fields.

        This widget is identical to the :meth:`form` box, except that
        all text fields are treated as :meth:`passwordbox` widgets
        rather than :meth:`inputbox` widgets.

        By default (as in :program:`dialog`), nothing is echoed to the
        terminal as the user types in the invisible fields. This can be
        confusing to users. Use ``insecure=True`` (keyword argument) if
        you want an asterisk to be echoed for each character entered by
        the user.

        Notable exceptions:

          - :exc:`BadPythonDialogUsage`
          - any exception raised by :meth:`Dialog._perform`

        """
        return self._generic_form("passwordform", "passwordform", text,
                                  elements, height, width, form_height,
                                  **kwargs)

    @widget
    def mixedform(self, text, elements, height=0, width=0, form_height=0,
                  **kwargs):
        """Display a form consisting of labels and fields.

        :param str text:        text to display in the box
        :param elements:        sequence describing the labels and
                                fields (see below)
        :param int height:      height of the box
        :param int width:       width of the box
        :param int form_height: number of form lines displayed at the
                                same time
        :return: a tuple of the form :samp:`({code}, {list})` where:

          - *code* is a :term:`Dialog exit code`;
          - *list* gives the contents of every field on exit, with the
            same order as in *elements*.

        :rtype: tuple

        A :meth:`!mixedform` box is very similar to a :meth:`form` box,
        and differs from the latter by allowing field attributes to be
        specified.

        Each element of *elements* must itself be a sequence
        :samp:`({label}, {yl}, {xl}, {item}, {yi}, {xi}, {field_length},
        {input_length}, {attributes})` containing the various parameters
        concerning a given field and the associated label.

        *attributes* is an integer interpreted as a bit mask with the
        following meaning (bit 0 being the least significant bit):

        +------------+-----------------------------------------------+
        | Bit number |                    Meaning                    |
        +============+===============================================+
        |     0      | the field should be hidden (e.g., a password) |
        +------------+-----------------------------------------------+
        |     1      | the field should be read-only (e.g., a label) |
        +------------+-----------------------------------------------+

        For all other parameters, please refer to the documentation of
        the :meth:`form` box.

        The return value is the same as would be with the :meth:`!form`
        box, except that fields marked as read-only with bit 1 of
        *attributes* are also included in the output list.

        Notable exceptions:

          - :exc:`BadPythonDialogUsage`
          - any exception raised by :meth:`Dialog._perform`

        """
        return self._generic_form("mixedform", "mixedform", text, elements,
                                  height, width, form_height, **kwargs)

    @widget
    def dselect(self, filepath, height=0, width=0, **kwargs):
        """Display a directory selection dialog box.

        :param str filepath: initial path
        :param int height:   height of the box
        :param int width:    width of the box
        :return: a tuple of the form :samp:`({code}, {path})` where:

          - *code* is a :term:`Dialog exit code`;
          - *path* is the directory chosen by the user.

        :rtype: tuple

        The directory selection dialog displays a text entry window
        in which you can type a directory, and above that a window
        with directory names.

        Here, *filepath* can be a path to a file, in which case the
        directory window will display the contents of the path and the
        text entry window will contain the preselected directory.

        Use :kbd:`Tab` or the arrow keys to move between the windows.
        Within the directory window, use the :kbd:`Up` and :kbd:`Down`
        arrow keys to scroll the current selection. Use the :kbd:`Space`
        bar to copy the current selection into the text entry window.

        Typing any printable character switches focus to the text entry
        window, entering that character as well as scrolling the
        directory window to the closest match.

        Use :kbd:`Enter` or the :guilabel:`OK` button to accept the
        current value in the text entry window and exit.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        # The help output does not depend on whether --help-status was passed
        # (dialog 1.2-20130902).
        return self._widget_with_string_output(
            ["--dselect", filepath, str(height), str(width)],
            kwargs, raw_help=True)

    @widget
    def editbox(self, filepath, height=0, width=0, **kwargs):
        """Display a basic text editor dialog box.

        :param str filepath: path to a file which determines the initial
                             contents of the dialog box
        :param int height:   height of the box
        :param int width:    width of the box
        :return: a tuple of the form :samp:`({code}, {text})` where:

          - *code* is a :term:`Dialog exit code`;
          - *text* is the contents of the text entry window on exit.

        :rtype: tuple

        The :meth:`!editbox` dialog displays a copy of the file
        contents. You may edit it using the :kbd:`Backspace`,
        :kbd:`Delete` and cursor keys to correct typing errors. It also
        recognizes :kbd:`Page Up` and :kbd:`Page Down`. Unlike the
        :meth:`inputbox`, you must tab to the :guilabel:`OK` or
        :guilabel:`Cancel` buttons to close the dialog. Pressing the
        :kbd:`Enter` key within the box will split the corresponding
        line.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        .. seealso:: method :meth:`editbox_str`

        """
        return self._widget_with_string_output(
            ["--editbox", filepath, str(height), str(width)],
            kwargs)

    def editbox_str(self, init_contents, *args, **kwargs):
        """
        Display a basic text editor dialog box (wrapper around :meth:`editbox`).

        :param str init_contents:
                          initial contents of the dialog box
        :param args:      positional arguments to pass to :meth:`editbox`
        :param kwargs:    keyword arguments to pass to :meth:`editbox`
        :return: a tuple of the form :samp:`({code}, {text})` where:

          - *code* is a :term:`Dialog exit code`;
          - *text* is the contents of the text entry window on exit.

        :rtype: tuple

        The :meth:`!editbox_str` method is a thin wrapper around
        :meth:`editbox`. :meth:`!editbox_str` accepts a string as its
        first argument, instead of a file path. That string is written
        to a temporary file whose path is passed to :meth:`!editbox`
        along with the arguments specified via *args* and *kwargs*.
        Please refer to :meth:`!editbox`\'s documentation for more
        details.

        Notes:

          - the temporary file is deleted before the method returns;
          - if *init_contents* does not end with a newline character
            (``'\\n'``), then this method automatically adds one. This
            is done in order to avoid unexpected behavior resulting from
            the fact that, before version 1.3-20160209,
            :program:`dialog`\'s editbox widget ignored the last line of
            the input file unless it was terminated by a newline
            character.

        Notable exceptions:

          - :exc:`PythonDialogOSError`
          - any exception raised by :meth:`Dialog._perform`

        .. versionadded:: 3.4

        .. seealso:: method :meth:`editbox`

        """
        if not init_contents.endswith('\n'):
            # Before version 1.3-20160209, dialog's --editbox widget
            # doesn't read the last line of the input file unless it
            # ends with a '\n' character.
            init_contents += '\n'

        with _OSErrorHandling():
            tmpfile = tempfile.NamedTemporaryFile(
                mode="w", prefix="pythondialog.tmp", delete=False)
            try:
                with tmpfile as f:
                    f.write(init_contents)
                # The temporary file is now closed. According to the tempfile
                # module documentation, this is necessary if we want to be able
                # to reopen it reliably regardless of the platform.

                res = self.editbox(tmpfile.name, *args, **kwargs)
            finally:
                # The test should always succeed, but I prefer being on the
                # safe side.
                if os.path.exists(tmpfile.name):
                    os.unlink(tmpfile.name)

        return res

    @widget
    def fselect(self, filepath, height=0, width=0, **kwargs):
        """Display a file selection dialog box.

        :param str filepath: initial path
        :param int height:   height of the box
        :param int width:    width of the box
        :return: a tuple of the form :samp:`({code}, {path})` where:

          - *code* is a :term:`Dialog exit code`;
          - *path* is the path chosen by the user (the last element of
            which may be a directory or a file).

        :rtype: tuple

        The file selection dialog displays a text entry window in
        which you can type a file name (or directory), and above that
        two windows with directory names and file names.

        Here, *filepath* can be a path to a file, in which case the file
        and directory windows will display the contents of the path and
        the text entry window will contain the preselected file name.

        Use :kbd:`Tab` or the arrow keys to move between the windows.
        Within the directory or file name windows, use the :kbd:`Up` and
        :kbd:`Down` arrow keys to scroll the current selection. Use the
        :kbd:`Space` bar to copy the current selection into the text
        entry window.

        Typing any printable character switches focus to the text entry
        window, entering that character as well as scrolling the
        directory and file name windows to the closest match.

        Use :kbd:`Enter` or the :guilabel:`OK` button to accept the
        current value in the text entry window, or the
        :guilabel:`Cancel` button to cancel.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        # The help output does not depend on whether --help-status was passed
        # (dialog 1.2-20130902).
        return self._widget_with_string_output(
            ["--fselect", filepath, str(height), str(width)],
            kwargs, strip_xdialog_newline=True, raw_help=True)

    def gauge_start(self, text="", height=None, width=None, percent=0,
                    **kwargs):
        """Display a gauge box.

        :param str text:    text to display in the box
        :param height:      height of the box
        :type height:       int or ``None``
        :param width:       width of the box
        :type width:        int or ``None``
        :param int percent: initial percentage shown in the meter
        :return:            undefined

        A gauge box displays a meter along the bottom of the box. The
        meter indicates a percentage.

        This function starts the :program:`dialog`-like program, telling
        it to display a gauge box containing a text and an initial
        percentage in the meter.


        .. rubric:: Gauge typical usage

        Gauge typical usage (assuming that *d* is an instance of the
        :class:`Dialog` class) looks like this::

            d.gauge_start()
            # do something
            d.gauge_update(10)       # 10% of the whole task is done
            # ...
            d.gauge_update(100, "any text here") # work is done
            exit_code = d.gauge_stop()           # cleanup actions


        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=8, width=54``.

        Notable exceptions:

          - any exception raised by :meth:`_call_program`
          - :exc:`PythonDialogOSError`

        """
        height, width = self._default_size((height, width), (8, 54))
        with _OSErrorHandling():
            # We need a pipe to send data to the child (dialog) process's
            # stdin while it is running.
            # rfd = File Descriptor for Reading
            # wfd = File Descriptor for Writing
            (child_stdin_rfd, child_stdin_wfd)  = os.pipe()

            child_pid, child_output_rfd, args_file = self._call_program(
                ["--gauge", text, str(height), str(width), str(percent)],
                redir_child_stdin_from_fd=child_stdin_rfd,
                close_fds=(child_stdin_wfd,), **kwargs)

            # fork() is done. We don't need child_stdin_rfd in the father
            # process anymore.
            os.close(child_stdin_rfd)

            self._gauge_process = {
                "pid": child_pid,
                "stdin": os.fdopen(child_stdin_wfd, "w"),
                "child_output_rfd": child_output_rfd,
                "args_file": args_file
                }

    def gauge_update(self, percent, text="", update_text=False):
        """Update a running gauge box.

        :param int percent:      new percentage to show in the gauge
                                 meter
        :param str text:         new text to optionally display in the
                                 box
        :param bool update_text: whether to update the text in the box
        :return:                 undefined

        This function updates the percentage shown by the meter of a
        running gauge box (meaning :meth:`gauge_start` must have been
        called previously). If *update_text* is ``True``, the text
        displayed in the box is also updated.

        See the :meth:`gauge_start` method documentation for information
        about how to use a gauge.

        Notable exception:

          :exc:`PythonDialogIOError` (:exc:`PythonDialogOSError` from
          Python 3.3 onwards) can be raised if there is an I/O error
          while trying to write to the pipe used to talk to the
          :program:`dialog`-like program.

        """
        if not isinstance(percent, int):
            raise BadPythonDialogUsage(
                "the 'percent' argument of gauge_update() must be an integer, "
                "but {0!r} is not".format(percent))

        if update_text:
            gauge_data = "XXX\n{0}\n{1}\nXXX\n".format(percent, text)
        else:
            gauge_data = "{0}\n".format(percent)
        with _OSErrorHandling():
            self._gauge_process["stdin"].write(gauge_data)
            self._gauge_process["stdin"].flush()

    # For "compatibility" with the old dialog.py...
    def gauge_iterate(*args, **kwargs):
        """Update a running gauge box.

        .. deprecated:: 2.03
          Use :meth:`gauge_update` instead.

        """
        warnings.warn("Dialog.gauge_iterate() has been obsolete for "
                      "many years", DeprecationWarning)
        gauge_update(*args, **kwargs)

    @widget
    @retval_is_code
    def gauge_stop(self):
        """Terminate a running gauge widget.

        :return:         a :term:`Dialog exit code`
        :rtype:          str

        This function performs the appropriate cleanup actions to
        terminate a running gauge started with :meth:`gauge_start`.

        See the :meth:`!gauge_start` method documentation for
        information about how to use a gauge.

        Notable exceptions:

          - any exception raised by :meth:`_handle_program_exit`;
          - :exc:`PythonDialogIOError` (:exc:`PythonDialogOSError` from
            Python 3.3 onwards) can be raised if closing the pipe used
            to talk to the :program:`dialog`-like program fails.

        """
        p = self._gauge_process
        # Close the pipe that we are using to feed dialog's stdin
        with _OSErrorHandling():
            p["stdin"].close()
        # According to dialog(1), the output should always be empty.
        exit_code = self._handle_program_exit(p["pid"],
                                              p["child_output_rfd"],
                                              p["args_file"])[0]
        return exit_code

    @widget
    @retval_is_code
    def infobox(self, text, height=None, width=None, **kwargs):
        """Display an information dialog box.

        :param str text: text to display in the box
        :param height:   height of the box
        :type height:    int or ``None``
        :param width:    width of the box
        :type width:     int or ``None``
        :return:         a :term:`Dialog exit code`
        :rtype:          str

        An info box is basically a message box. However, in this case,
        :program:`dialog` will exit immediately after displaying the
        message to the user. The screen is not cleared when
        :program:`dialog` exits, so that the message will remain on the
        screen after the method returns. This is useful when you want to
        inform the user that some operations are carrying on that may
        require some time to finish.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=10, width=30``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (10, 30))
        return self._widget_with_no_output(
            "infobox",
            ["--infobox", text, str(height), str(width)],
            kwargs)

    @widget
    def inputbox(self, text, height=None, width=None, init='', **kwargs):
        """Display an input dialog box.

        :param str text: text to display in the box
        :param height:   height of the box
        :type height:    int or ``None``
        :param width:    width of the box
        :type width:     int or ``None``
        :param str init: default input string
        :return: a tuple of the form :samp:`({code}, {string})` where:

          - *code* is a :term:`Dialog exit code`;
          - *string* is the string entered by the user.

        :rtype: tuple

        An input box is useful when you want to ask questions that
        require the user to input a string as the answer. If *init* is
        supplied, it is used to initialize the input string. When
        entering the string, the :kbd:`Backspace` key can be used to
        correct typing errors. If the input string is longer than can
        fit in the dialog box, the input field will be scrolled.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=10, width=30``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (10, 30))
        # The help output does not depend on whether --help-status was passed
        # (dialog 1.2-20130902).
        return self._widget_with_string_output(
            ["--inputbox", text, str(height), str(width), init],
            kwargs, strip_xdialog_newline=True, raw_help=True)

    @widget
    def inputmenu(self, text, height=0, width=None, menu_height=None,
                  choices=[], **kwargs):
        """Display an inputmenu dialog box.

        :param str text:    text to display in the box
        :param int height:  height of the box
        :param width:       width of the box
        :type width:        int or ``None``
        :param menu_height: height of the menu (scrollable part)
        :type menu_height:  int or ``None``
        :param choices:     an iterable of :samp:`({tag}, {item})`
                            tuples, the meaning of which is explained
                            below
        :return:            see :ref:`below <inputmenu-return-value>`


        .. rubric:: Overview

        An :meth:`!inputmenu` box is a dialog box that can be used to
        present a list of choices in the form of a menu for the user to
        choose. Choices are displayed in the given order. The main
        differences with the :meth:`menu` dialog box are:

          - entries are not automatically centered, but left-adjusted;

          - the current entry can be renamed by pressing the
            :guilabel:`Rename` button, which allows editing the *item*
            part of the current entry.

        Each menu entry consists of a *tag* string and an *item* string.
        The :dfn:`tag` gives the entry a name to distinguish it from the
        other entries in the menu and to provide quick keyboard access.
        The :dfn:`item` is a short description of the option that the
        entry represents.

        The user can move between the menu entries by pressing the
        :kbd:`Up` and :kbd:`Down` arrow keys or the first letter of the
        tag as a hot key. There are *menu_height* lines (not entries!)
        displayed in the scrollable part of the menu at one time.

        At the time of this writing (with :program:`dialog`
        1.2-20140219), it is not possible to add an Extra button to this
        widget, because internally, the :guilabel:`Rename` button *is*
        the Extra button.

        .. note::

          It is strongly advised not to put any space in tags, otherwise
          the :program:`dialog` output can be ambiguous if the
          corresponding entry is renamed, causing pythondialog to return
          a wrong tag string and new item text.

          The reason is that in this case, the :program:`dialog` output
          is :samp:`RENAMED {tag} {item}` and pythondialog cannot guess
          whether spaces after the :samp:`RENAMED` + *space* prefix
          belong to the *tag* or the new *item* text.

        .. note::

          There is no point in calling this method with
          ``help_status=True``, because it is not possible to rename
          several items nor is it possible to choose the
          :guilabel:`Help` button (or any button other than
          :guilabel:`Rename`) once one has started to rename an item.

        .. _inputmenu-return-value:

        .. rubric:: Return value

        Return a tuple of the form :samp:`({exit_info}, {tag},
        {new_item_text})` where:

          + *exit_info* is either:

            - the string ``"accepted"``, meaning that an entry was
              accepted without renaming;
            - the string ``"renamed"``, meaning that an entry was
              accepted after being renamed;
            - one of the standard :term:`Dialog exit codes <Dialog exit
              code>` :attr:`Dialog.CANCEL`, :attr:`Dialog.ESC` or
              :attr:`Dialog.HELP` (:attr:`Dialog.EXTRA` can't be
              returned, because internally, the :guilabel:`Rename`
              button *is* the Extra button).

          + *tag* indicates which entry was accepted (with or without
            renaming), if any. If no entry was accepted (e.g., if the
            dialog was exited with the :guilabel:`Cancel` button), then
            *tag* is ``None``.

          + *new_item_text* gives the new *item* part of the renamed
            entry if *exit_info* is ``"renamed"``, otherwise it is
            ``None``.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=0, width=60, menu_height=7``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        width, menu_height = self._default_size((width, menu_height), (60, 7))
        cmd = ["--inputmenu", text, str(height), str(width), str(menu_height)]
        for t in choices:
            cmd.extend(t)
        (code, output) = self._perform(cmd, **kwargs)

        if code == self.HELP:
            help_id = self._parse_help(output, kwargs)
            return (code, help_id, None)
        elif code == self.OK:
            return ("accepted", output, None)
        elif code == self.EXTRA:
            if not output.startswith("RENAMED "):
                raise PythonDialogBug(
                    "'output' does not start with 'RENAMED ': {0!r}".format(
                        output))
            t = output.split(' ', 2)
            return ("renamed", t[1], t[2])
        else:
            return (code, None, None)

    @widget
    def menu(self, text, height=None, width=None, menu_height=None, choices=[],
             **kwargs):
        """Display a menu dialog box.

        :param str text:        text to display in the box
        :param height:      height of the box
        :type height:       int or ``None``
        :param width:       width of the box
        :type width:        int or ``None``
        :param menu_height: number of entries displayed in the box
                            (which can be scrolled) at a given time
        :type menu_height:  int or ``None``
        :param choices:     an iterable of :samp:`({tag}, {item})`
                            tuples, the meaning of which is explained
                            below
        :return: a tuple of the form :samp:`({code}, {tag})` where:

          - *code* is a :term:`Dialog exit code`;
          - *tag* is the tag string corresponding to the item that the
            user chose.

        :rtype: tuple

        As its name suggests, a :meth:`!menu` box is a dialog box that
        can be used to present a list of choices in the form of a menu
        for the user to choose. Choices are displayed in the given
        order.

        Each menu entry consists of a *tag* string and an *item* string.
        The :dfn:`tag` gives the entry a name to distinguish it from the
        other entries in the menu and to provide quick keyboard access.
        The :dfn:`item` is a short description of the option that the
        entry represents.

        The user can move between the menu entries by pressing the
        :kbd:`Up` and :kbd:`Down` arrow keys, the first letter of the
        tag as a hotkey, or the number keys :kbd:`1` through :kbd:`9`.
        There are *menu_height* entries displayed in the menu at one
        time, but it will be scrolled if there are more entries than
        that.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=15, width=54, menu_height=7``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width, menu_height = self._default_size(
            (height, width, menu_height), (15, 54, 7))
        cmd = ["--menu", text, str(height), str(width), str(menu_height)]
        for t in choices:
            cmd.extend(t)

        return self._widget_with_string_output(
            cmd, kwargs, strip_xdialog_newline=True)

    @widget
    @retval_is_code
    def mixedgauge(self, text, height=0, width=0, percent=0, elements=[],
             **kwargs):
        """Display a mixed gauge dialog box.

        :param str text:    text to display in the middle of the box,
                            between the elements list and the progress
                            bar
        :param int height:  height of the box
        :param int width:   width of the box
        :param int percent: integer giving the percentage for the global
                            progress bar
        :param elements:    an iterable of :samp:`({tag}, {item})`
                            tuples, the meaning of which is explained
                            below
        :return:            a :term:`Dialog exit code`
        :rtype:             str

        A :meth:`!mixedgauge` box displays a list of "elements" with
        status indication for each of them, followed by a text and
        finally a global progress bar along the bottom of the box.

        The top part ("elements") is suitable for displaying a task
        list. One element is displayed per line, with its *tag* part on
        the left and its *item* part on the right. The *item* part is a
        string that is displayed on the right of the same line.

        The *item* part of an element can be an arbitrary string.
        Special values listed in the :manpage:`dialog(3)` manual page
        are translated into a status indication for the corresponding
        task (*tag*), such as: "Succeeded", "Failed", "Passed",
        "Completed", "Done", "Skipped", "In Progress", "Checked", "N/A"
        or a progress bar.

        A progress bar for an element is obtained by supplying a
        negative number for the *item*. For instance, ``"-75"`` will
        cause a progress bar indicating 75% to be displayed on the
        corresponding line.

        For your convenience, if an *item* appears to be an integer or a
        float, it will be converted to a string before being passed to
        the :program:`dialog`-like program.

        *text* is shown as a sort of caption between the list and the
        global progress bar. The latter displays *percent* as the
        percentage of completion.

        Contrary to the regular :ref:`gauge widget <gauge-widget>`,
        :meth:`!mixedgauge` is completely static. You have to call
        :meth:`!mixedgauge` several times in order to display different
        percentages in the global progress bar or various status
        indicators for a given task.

        .. note::

           Calling :meth:`!mixedgauge` several times is likely to cause
           unwanted flickering because of the screen initializations
           performed by :program:`dialog` on every run.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        cmd = ["--mixedgauge", text, str(height), str(width), str(percent)]
        for t in elements:
            cmd.extend( (t[0], str(t[1])) )
        return self._widget_with_no_output("mixedgauge", cmd, kwargs)

    @widget
    @retval_is_code
    def msgbox(self, text, height=None, width=None, **kwargs):
        """Display a message dialog box, with scrolling and line wrapping.

        :param str text: text to display in the box
        :param height:   height of the box
        :type height:    int or ``None``
        :param width:    width of the box
        :type width:     int or ``None``
        :return:         a :term:`Dialog exit code`
        :rtype:          str

        Display *text* in a message box, with a scrollbar and percentage
        indication if *text* is too long to fit in a single "screen".

        An :meth:`!msgbox` is very similar to a :meth:`yesno` box. The
        only difference between an :meth:`!msgbox` and a :meth:`!yesno`
        box is that the former only has a single :guilabel:`OK` button.
        You can use :meth:`!msgbox` to display any message you like.
        After reading the message, the user can press the :kbd:`Enter`
        key so that :program:`dialog` will exit and the calling program
        can continue its operation.

        :meth:`!msgbox` performs automatic line wrapping. If you want to
        force a newline at some point, simply insert it in *text*. In
        other words (with the default settings), newline characters in
        *text* **are** respected; the line wrapping process performed by
        :program:`dialog` only inserts **additional** newlines when
        needed. If you want no automatic line wrapping, consider using
        :meth:`scrollbox`.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=10, width=30``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (10, 30))
        return self._widget_with_no_output(
            "msgbox",
            ["--msgbox", text, str(height), str(width)],
            kwargs)

    @widget
    @retval_is_code
    def pause(self, text, height=None, width=None, seconds=5, **kwargs):
        """Display a pause dialog box.

        :param str text:    text to display in the box
        :param height:      height of the box
        :type height:       int or ``None``
        :param width:       width of the box
        :type width:        int or ``None``
        :param int seconds: number of seconds to pause for
        :return:
          a :term:`Dialog exit code` (which is :attr:`Dialog.OK` if the
          widget ended automatically after *seconds* seconds or if the
          user pressed the :guilabel:`OK` button)
        :rtype:             str

        A :meth:`!pause` box displays a text and a meter along the
        bottom of the box, during a specified amount of time
        (*seconds*). The meter indicates how many seconds remain until
        the end of the pause. The widget exits when the specified number
        of seconds is elapsed, or immediately if the user presses the
        :guilabel:`OK` button, the :guilabel:`Cancel` button or the
        :kbd:`Esc` key.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=15, width=60``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (15, 60))
        return self._widget_with_no_output(
            "pause",
            ["--pause", text, str(height), str(width), str(seconds)],
            kwargs)

    @widget
    def passwordbox(self, text, height=None, width=None, init='', **kwargs):
        """Display a password input dialog box.

        :param str text:  text to display in the box
        :param height:    height of the box
        :type height:     int or ``None``
        :param width:     width of the box
        :type width:      int or ``None``
        :param str init:  default input password
        :return: a tuple of the form :samp:`({code}, {password})` where:

          - *code* is a :term:`Dialog exit code`;
          - *password* is the password entered by the user.

        :rtype: tuple

        A :meth:`!passwordbox` is similar to an :meth:`inputbox`, except
        that the text the user enters is not displayed. This is useful
        when prompting for passwords or other sensitive information. Be
        aware that if anything is passed in *init*, it will be visible
        in the system's process table to casual snoopers. Also, it is
        very confusing to the user to provide them with a default
        password they cannot see. For these reasons, using *init* is
        highly discouraged.

        By default (as in :program:`dialog`), nothing is echoed to the
        terminal as the user enters the sensitive text. This can be
        confusing to users. Use ``insecure=True`` (keyword argument) if
        you want an asterisk to be echoed for each character entered by
        the user.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=10, width=60``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (10, 60))
        # The help output does not depend on whether --help-status was passed
        # (dialog 1.2-20130902).
        return self._widget_with_string_output(
            ["--passwordbox", text, str(height), str(width), init],
            kwargs, strip_xdialog_newline=True, raw_help=True)

    def _progressboxoid(self, widget, file_path=None, file_flags=os.O_RDONLY,
                        fd=None, text=None, height=20, width=78, **kwargs):
        if (file_path is None and fd is None) or \
                (file_path is not None and fd is not None):
            raise BadPythonDialogUsage(
                "{0}.{1}.{2}: either 'file_path' or 'fd' must be provided, and "
                "not both at the same time".format(
                    __name__, self.__class__.__name__, widget))

        with _OSErrorHandling():
            if file_path is not None:
                if fd is not None:
                    raise PythonDialogBug(
                        "unexpected non-None value for 'fd': {0!r}".format(fd))
                # No need to pass 'mode', as the file is not going to be
                # created here.
                fd = os.open(file_path, file_flags)

            try:
                args = [ "--{0}".format(widget) ]
                if text is not None:
                    args.append(text)
                args.extend([str(height), str(width)])

                kwargs["redir_child_stdin_from_fd"] = fd
                code = self._widget_with_no_output(widget, args, kwargs)
            finally:
                with _OSErrorHandling():
                    if file_path is not None:
                        # We open()ed file_path ourselves, let's close it now.
                        os.close(fd)

        return code

    @widget
    @retval_is_code
    def progressbox(self, file_path=None, file_flags=os.O_RDONLY,
                    fd=None, text=None, height=None, width=None, **kwargs):
        """
        Display a possibly growing stream in a dialog box, as with ``tail -f``.

        A file, or more generally a stream that can be read from, must
        be specified with either:

        :param str file_path: path to the file that is going to be displayed
        :param file_flags:
          flags used when opening *file_path*; those are passed to
          :func:`os.open` (not the built-in :func:`open` function!). By
          default, only one flag is set: :data:`os.O_RDONLY`.

        or

        :param int fd: file descriptor for the stream to be displayed

        Remaining parameters:

        :param text:   caption continuously displayed at the top, above
                       the stream text, or ``None`` to disable the
                       caption
        :param height: height of the box
        :type height:  int or ``None``
        :param width:  width of the box
        :type width:   int or ``None``
        :return:       a :term:`Dialog exit code`
        :rtype:        str

        Display the contents of the specified file, updating the dialog
        box whenever the file grows, as with the ``tail -f`` command.

        The file can be specified in two ways:

          - either by giving its path (and optionally :func:`os.open`
            flags) with parameters *file_path* and *file_flags*;

          - or by passing its file descriptor with parameter *fd* (in
            which case it may not even be a file; for instance, it could
            be an anonymous pipe created with :func:`os.pipe`).

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=20, width=78``.

        Notable exceptions:

          - :exc:`PythonDialogOSError` (:exc:`PythonDialogIOError` if
            the Python version is < 3.3)
          - any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (20, 78))
        return self._progressboxoid(
            "progressbox", file_path=file_path, file_flags=file_flags,
            fd=fd, text=text, height=height, width=width, **kwargs)

    @widget
    @retval_is_code
    def programbox(self, file_path=None, file_flags=os.O_RDONLY,
                   fd=None, text=None, height=None, width=None, **kwargs):
        """
        Display a possibly growing stream in a dialog box, as with ``tail -f``.

        A :meth:`!programbox` is very similar to a :meth:`progressbox`.
        The only difference between a :meth:`!programbox` and a
        :meth:`!progressbox` is that a :meth:`!programbox` displays an
        :guilabel:`OK` button, but only after the input stream has been
        exhausted (i.e., *End Of File* has been reached).

        This dialog box can be used to display the piped output of an
        external program. After the program completes, the user can
        press the :kbd:`Enter` key to close the dialog and resume
        execution of the calling program.

        The parameters and exceptions are the same as for
        :meth:`progressbox`. Please refer to the corresponding
        documentation.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=20, width=78``.

        This widget requires :program:`dialog` >= 1.1-20110302.

        .. versionadded:: 2.14

        """
        self._dialog_version_check("1.1-20110302", "the programbox widget")

        height, width = self._default_size((height, width), (20, 78))
        return self._progressboxoid(
            "programbox", file_path=file_path, file_flags=file_flags,
            fd=fd, text=text, height=height, width=width, **kwargs)

    @widget
    def radiolist(self, text, height=None, width=None, list_height=None,
                  choices=[], **kwargs):
        """Display a radiolist box.

        :param str text:    text to display in the box
        :param height:      height of the box
        :type height:       int or ``None``
        :param width:       width of the box
        :type width:        int or ``None``
        :param list_height: number of entries displayed in the box
                            (which can be scrolled) at a given time
        :type list_height:  int or ``None``
        :param choices:
          an iterable of :samp:`({tag}, {item}, {status})` tuples
          where *status* specifies the initial selected/unselected
          state of each entry; can be ``True`` or ``False``, ``1`` or
          ``0``, ``"on"`` or ``"off"`` (``True``, ``1`` and ``"on"``
          meaning selected), or any case variation of these two
          strings. No more than one entry should be set to ``True``.
        :return: a tuple of the form :samp:`({code}, {tag})` where:

          - *code* is a :term:`Dialog exit code`;
          - *tag* is the tag string corresponding to the entry that was
            chosen by the user.

        :rtype: tuple

        A :meth:`!radiolist` box is similar to a :meth:`menu` box. The
        main differences are presentation and that the
        :meth:`!radiolist` allows you to indicate which entry is
        initially selected, by setting its status to ``True``.

        If the user exits with :kbd:`Esc` or :guilabel:`Cancel`, or if
        all entries were initially set to ``False`` and not altered
        before the user chose :guilabel:`OK`, the returned tag is the
        empty string.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=15, width=54, list_height=7``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform` or :func:`_to_onoff`

        """
        height, width, list_height = self._default_size(
            (height, width, list_height), (15, 54, 7))

        cmd = ["--radiolist", text, str(height), str(width), str(list_height)]
        for t in choices:
            cmd.extend([ t[0], t[1], _to_onoff(t[2]) ] + list(t[3:]))
        (code, output) = self._perform(cmd, **kwargs)

        output = self._strip_xdialog_newline(output)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs)
            if self._help_status_on(kwargs):
                help_id, selected_tag = help_data
                # Reconstruct 'choices' with the selected item inferred from
                # 'selected_tag'.
                choices = [ [ tag, item, tag == selected_tag ] + rest for
                            (tag, item, status, *rest) in choices ]
                return (code, (help_id, selected_tag, choices))
            else:
                return (code, help_data)
        else:
            return (code, output)

    @widget
    def rangebox(self, text, height=0, width=0, min=None, max=None, init=None,
                 **kwargs):
        """Display a range dialog box.

        :param str text:   text to display above the actual range control
        :param int height: height of the box
        :param int width:  width of the box
        :param int min:    minimum value for the range control
        :param int max:    maximum value for the range control
        :param int init:   initial value for the range control
        :return: a tuple of the form :samp:`({code}, {val})` where:

          - *code* is a :term:`Dialog exit code`;
          - *val* is an integer: the value chosen by the user.

        :rtype: tuple

        The :meth:`!rangebox` dialog allows the user to select from a
        range of integers using a kind of slider. The range control
        shows the current value as a bar (like the :ref:`gauge dialog
        <gauge-widget>`).

        The :kbd:`Tab` and arrow keys move the cursor between the
        buttons and the range control. When the cursor is on the latter,
        you can change the value with the following keys:

        +-----------------------+----------------------------+
        |          Key          |           Action           |
        +=======================+============================+
        | :kbd:`Left` and       | select a digit to modify   |
        | :kbd:`Right` arrows   |                            |
        +-----------------------+----------------------------+
        | :kbd:`+` / :kbd:`-`   | increment/decrement the    |
        |                       | selected digit by one unit |
        +-----------------------+----------------------------+
        | :kbd:`0`–:kbd:`9`     | set the selected digit to  |
        |                       | the given value            |
        +-----------------------+----------------------------+

        Some keys are also recognized in all cursor positions:

        +------------------+--------------------------------------+
        |       Key        |                Action                |
        +==================+======================================+
        | :kbd:`Home` /    | set the value to its minimum or      |
        | :kbd:`End`       | maximum                              |
        +------------------+--------------------------------------+
        | :kbd:`Page Up` / | decrement/increment the value so     |
        | :kbd:`Page Down` | that the slider moves by one column  |
        +------------------+--------------------------------------+

        This widget requires :program:`dialog` >= 1.2-20121230.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        .. versionadded:: 2.14

        """
        self._dialog_version_check("1.2-20121230", "the rangebox widget")

        for name in ("min", "max", "init"):
            if not isinstance(locals()[name], int):
                raise BadPythonDialogUsage(
                    "{0!r} argument not an int: {1!r}".format(name,
                                                              locals()[name]))
        (code, output) = self._perform(
            ["--rangebox", text] + [ str(i) for i in
                                     (height, width, min, max, init) ],
            **kwargs)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs, raw_format=True)
            # The help output does not depend on whether --help-status was
            # passed (dialog 1.2-20130902).
            return (code, int(help_data))
        elif code in (self.OK, self.EXTRA):
            return (code, int(output))
        else:
            return (code, None)

    @widget
    @retval_is_code
    def scrollbox(self, text, height=None, width=None, **kwargs):
        """Display a string in a scrollable box, with no line wrapping.

        :param str text: string to display in the box
        :param height:   height of the box
        :type height:    int or ``None``
        :param width:    width of the box
        :type width:     int or ``None``
        :return:         a :term:`Dialog exit code`
        :rtype:          str

        This method is a layer on top of :meth:`textbox`. The
        :meth:`!textbox` widget in :program:`dialog` allows one to
        display file contents only. This method can be used to display
        any text in a scrollable box. This is simply done by creating a
        temporary file, calling :meth:`!textbox` and deleting the
        temporary file afterwards.

        The text is not automatically wrapped. New lines in the
        scrollable box will be placed exactly as in *text*. If you want
        automatic line wrapping, you should use the :meth:`msgbox`
        widget instead (the :mod:`textwrap` module from the Python
        standard library is also worth knowing about).

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=20, width=78``.

        Notable exceptions:

          :exc:`PythonDialogOSError` (:exc:`PythonDialogIOError` if the
          Python version is < 3.3)

        .. versionchanged:: 3.1
           :exc:`UnableToCreateTemporaryDirectory` exception can't be
           raised anymore. The equivalent condition now raises
           :exc:`PythonDialogOSError`.

        """
        height, width = self._default_size((height, width), (20, 78))

        with _OSErrorHandling():
            tmpfile = tempfile.NamedTemporaryFile(
                mode="w", prefix="pythondialog.tmp", delete=False)
            try:
                with tmpfile as f:
                    f.write(text)
                # The temporary file is now closed. According to the tempfile
                # module documentation, this is necessary if we want to be able
                # to reopen it reliably regardless of the platform.

                # Ask for an empty title unless otherwise specified
                if kwargs.get("title", None) is None:
                    kwargs["title"] = ""

                return self._widget_with_no_output(
                    "textbox",
                    ["--textbox", tmpfile.name, str(height), str(width)],
                    kwargs)
            finally:
                # The test should always succeed, but I prefer being on the
                # safe side.
                if os.path.exists(tmpfile.name):
                    os.unlink(tmpfile.name)

    @widget
    @retval_is_code
    def tailbox(self, filepath, height=None, width=None, **kwargs):
        """Display the contents of a file in a dialog box, as with ``tail -f``.

        :param str filepath: path to a file, the contents of which is to
                             be displayed in the box
        :param height:       height of the box
        :type height:        int or ``None``
        :param width:        width of the box
        :type width:         int or ``None``
        :return:             a :term:`Dialog exit code`
        :rtype:              str

        Display the contents of the file specified with *filepath*,
        updating the dialog box whenever the file grows, as with the
        ``tail -f`` command.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=20, width=60``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (20, 60))
        return self._widget_with_no_output(
            "tailbox",
            ["--tailbox", filepath, str(height), str(width)],
            kwargs)
    # No tailboxbg widget, at least for now.

    @widget
    @retval_is_code
    def textbox(self, filepath, height=None, width=None, **kwargs):
        """Display the contents of a file in a dialog box.

        :param str filepath: path to a file, the contents of which is to
                             be displayed in the box
        :param height:       height of the box
        :type height:        int or ``None``
        :param width:        width of the box
        :type width:         int or ``None``
        :return:             a :term:`Dialog exit code`
        :rtype:              str

        A :meth:`!textbox` lets you display the contents of a text file
        in a dialog box. It is like a simple text file viewer. The user
        can move through the file using the :kbd:`Up` and :kbd:`Down`
        arrow keys, :kbd:`Page Up` and :kbd:`Page Down` as well as the
        :kbd:`Home` and :kbd:`End` keys available on most keyboards. If
        the lines are too long to be displayed in the box, the
        :kbd:`Left` and :kbd:`Right` arrow keys can be used to scroll
        the text region horizontally. For more convenience, forward and
        backward search functions are also provided.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=20, width=60``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (20, 60))
        # This is for backward compatibility... not that it is
        # stupid, but I prefer explicit programming.
        if kwargs.get("title", None) is None:
            kwargs["title"] = filepath

        return self._widget_with_no_output(
            "textbox",
            ["--textbox", filepath, str(height), str(width)],
            kwargs)

    def _timebox_parse_time(self, time_str):
        try:
            mo = _timebox_time_cre.match(time_str)
        except re.error as e:
            raise PythonDialogReModuleError(str(e)) from e

        if not mo:
            raise UnexpectedDialogOutput(
                "the dialog-like program returned the following "
                "unexpected output (a time string was expected) with the "
                "--timebox option: {0!r}".format(time_str))

        return [ int(s) for s in mo.group("hour", "minute", "second") ]

    @widget
    def timebox(self, text, height=None, width=None, hour=-1, minute=-1,
                second=-1, **kwargs):
        """Display a time dialog box.

        :param str text:   text to display in the box
        :param height:     height of the box
        :type height:      int or ``None``
        :param int width:  width of the box
        :type width:       int or ``None``
        :param int hour:   inititial hour selected
        :param int minute: inititial minute selected
        :param int second: inititial second selected
        :return: a tuple of the form :samp:`({code}, {time})` where:

          - *code* is a :term:`Dialog exit code`;
          - *time* is a list of the form :samp:`[{hour}, {minute},
            {second}]`, where *hour*, *minute* and *second* are integers
            corresponding to the time chosen by the user.

        :rtype: tuple

        :meth:`timebox` is a dialog box which allows one to select an
        hour, minute and second. If any of the values for *hour*,
        *minute* and *second* is negative, the current time's
        corresponding value is used. You can increment or decrement any
        of those using the :kbd:`Left`, :kbd:`Up`, :kbd:`Right` and
        :kbd:`Down` arrows. Use :kbd:`Tab` or :kbd:`Backtab` to move
        between windows.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=3, width=30``.

        Notable exceptions:

          - any exception raised by :meth:`Dialog._perform`
          - :exc:`PythonDialogReModuleError`
          - :exc:`UnexpectedDialogOutput`

        """
        height, width = self._default_size((height, width), (3, 30))
        (code, output) = self._perform(
            ["--timebox", text, str(height), str(width),
               str(hour), str(minute), str(second)],
            **kwargs)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs, raw_format=True)
            # The help output does not depend on whether --help-status was
            # passed (dialog 1.2-20130902).
            return (code, self._timebox_parse_time(help_data))
        elif code in (self.OK, self.EXTRA):
            return (code, self._timebox_parse_time(output))
        else:
            return (code, None)

    @widget
    def treeview(self, text, height=0, width=0, list_height=0,
                 nodes=[], **kwargs):
        """Display a treeview box.

        :param str text:        text to display at the top of the box
        :param int height:      height of the box
        :param int width:       width of the box
        :param int list_height:
          number of lines reserved for the main part of the box,
          where the tree is displayed
        :param nodes:
          an iterable of :samp:`({tag}, {item}, {status}, {depth})` tuples
          describing nodes, where:

            - *tag* is used to indicate which node was selected by
              the user on exit;
            - *item* is the text displayed for the node;
            - *status* specifies the initial selected/unselected
              state of each entry; can be ``True`` or ``False``,
              ``1`` or ``0``, ``"on"`` or ``"off"`` (``True``, ``1``
              and ``"on"`` meaning selected), or any case variation
              of these two strings;
            - *depth* is a non-negative integer indicating the depth
              of the node in the tree (``0`` for the root node).

        :return: a tuple of the form :samp:`({code}, {tag})` where:

          - *code* is a :term:`Dialog exit code`;
          - *tag* is the tag of the selected node.

        Display nodes organized in a tree structure. Each node has a
        *tag*, an *item* text, a selected *status*, and a *depth* in
        the tree. Only the *item* texts are displayed in the widget;
        *tag*\s are only used for the return value. Only one node can
        be selected at a given time, as for the :meth:`radiolist`
        widget.

        This widget requires :program:`dialog` >= 1.2-20121230.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform` or :func:`_to_onoff`

        .. versionadded:: 2.14

        """
        self._dialog_version_check("1.2-20121230", "the treeview widget")
        cmd = ["--treeview", text, str(height), str(width), str(list_height)]

        nselected = 0
        for i, t in enumerate(nodes):
            if not isinstance(t[3], int):
                raise BadPythonDialogUsage(
                    "fourth element of node {0} not an int: {1!r}".format(
                        i, t[3]))

            status = _to_onoff(t[2])
            if status == "on":
                nselected += 1

            cmd.extend([ t[0], t[1], status, str(t[3]) ] + list(t[4:]))

        if nselected != 1:
            raise BadPythonDialogUsage(
                "exactly one node must be selected, not {0}".format(nselected))

        (code, output) = self._perform(cmd, **kwargs)

        if code == self.HELP:
            help_data = self._parse_help(output, kwargs)
            if self._help_status_on(kwargs):
                help_id, selected_tag = help_data
                # Reconstruct 'nodes' with the selected item inferred from
                # 'selected_tag'.
                nodes = [ [ tag, item, tag == selected_tag ] + rest for
                          (tag, item, status, *rest) in nodes ]
                return (code, (help_id, selected_tag, nodes))
            else:
                return (code, help_data)
        elif code in (self.OK, self.EXTRA):
            return (code, output)
        else:
            return (code, None)

    @widget
    @retval_is_code
    def yesno(self, text, height=None, width=None, **kwargs):
        """Display a yes/no dialog box.

        :param str text: text to display in the box
        :param height:   height of the box
        :type height:    int or ``None``
        :param width:    width of the box
        :type width:     int or ``None``
        :return:         a :term:`Dialog exit code`
        :rtype:          str

        Display a dialog box containing *text* and two buttons labelled
        :guilabel:`Yes` and :guilabel:`No` by default.

        The box size is *height* rows by *width* columns. If *text* is
        too long to fit in one line, it will be automatically divided
        into multiple lines at appropriate places. *text* may also
        contain the substring ``"\\n"`` or newline characters to control
        line breaking explicitly.

        This :meth:`!yesno` dialog box is useful for asking questions
        that require the user to answer either "yes" or "no". These are
        the default button labels, however they can be freely set with
        the ``yes_label`` and ``no_label`` keyword arguments. The user
        can switch between the buttons by pressing the :kbd:`Tab` key.

        Default values for the size parameters when the
        :ref:`autowidgetsize <autowidgetsize>` option is disabled:
        ``height=10, width=30``.

        Notable exceptions:

          any exception raised by :meth:`Dialog._perform`

        """
        height, width = self._default_size((height, width), (10, 30))
        return self._widget_with_no_output(
            "yesno",
            ["--yesno", text, str(height), str(width)],
            kwargs)
