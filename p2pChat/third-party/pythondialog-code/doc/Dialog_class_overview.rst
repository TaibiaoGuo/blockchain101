.. currentmodule:: dialog

:class:`Dialog` class overview
==============================

Initializing a :class:`Dialog` instance
---------------------------------------

Since all widgets in pythondialog are implemented as methods of the
:class:`Dialog` class, a pythondialog-based application usually starts by
creating a :class:`!Dialog` instance.

.. autoclass:: Dialog
   :members: __init__

.. _autowidgetsize:

.. rubric:: About the *autowidgetsize* option

The *autowidgetsize* option should be convenient in situations where figuring
out suitable widget size parameters is a burden, for instance when developing
little scripts that don't need too much visual polishing, when a widget is
used to display data, the size of which is not easily predictable, or simply
when one doesn't want to hardcode the widget size.

This option is implemented in the following way: for a given size parameter
(for instance, *width*) of a given widget, the default value in the
widget-producing method is now ``None`` if it previously had a non-zero
default. At runtime, if the value seen by the widget-producing method is not
``None``, it is used as is; on the contrary, if that value is ``None``, it is
automatically replaced with:

  - ``0`` if the :class:`Dialog` instance has been initialized with
    *autowidgetsize* set to ``True``;
  - the old default otherwise, in order to preserve backward-comptability.

.. note::

  - the *autowidgetsize* option is currently marked as experimental, please
    give some feedback;
  - you may encounter questionable results if you only set one of the *width*
    and *height* parameters to ``0`` for a given widget (seen in
    :program:`dialog` 1.2-20140219).

.. warning::

  You should not explicitly pass ``None`` for a size parameter such as *width*
  or *height*. If you want a fixed size, specify it directly (as an int);
  otherwise, either use the *autowidgetsize* option or set the parameter to
  ``0`` (e.g., ``width=0``).


.. _passing-dialog-common-options:

Passing :program:`dialog` "common options"
------------------------------------------

Every widget method has a \*\*kwargs argument allowing you to pass
:term:`common options <dialog common options>` (see the :manpage:`dialog(1)`
manual page) to :program:`dialog` for this widget call. For instance, if *d*
is a :class:`Dialog` instance, you can write::

  d.checklist(args, ..., title="A Great Title", no_shadow=True)

The *no_shadow* option is worth looking at:

  #. It is an option that takes no argument as far as :program:`dialog` is
     concerned (unlike the :option:`--title` option, for instance). When you
     list it as a keyword argument, the option is really passed to
     :program:`dialog` only if the value you gave it evaluates to ``True`` in
     a boolean context. For instance, ``no_shadow=True`` will cause
     :option:`--no-shadow` to be passed to :program:`dialog` whereas
     ``no_shadow=False`` will cause this option not to be passed to
     :program:`dialog` at all.

  #. It is an option that has a hyphen (``-``) in its name, which you must
     change into an underscore (``_``) to pass it as a Python keyword
     argument. Therefore, :option:`--no-shadow` is passed by giving a
     ``no_shadow=True`` keyword argument to :class:`Dialog` methods (the
     leading two dashes are also consistently removed).

.. note::

   When :meth:`Dialog.__init__` is called with
   :samp:`{pass_args_via_file}=True` (or without any explicit setting for this
   option, and the pythondialog as well as :program:`dialog` versions are
   recent enough so that the option is enabled by default), then the options
   are not directly passed to :program:`dialog`. Instead, all options are
   written to a temporary file which :program:`dialog` is pointed to via
   :option:`--file`. This ensures better confidentiality with respect to other
   users of the same computer.


.. versionadded:: 2.14
   Support for the *default_button* and *no_tags* common options.

.. versionadded:: 3.0
   Proper support for the *extra_button*, *item_help* and *help_status* common
   options.


Return value of widget-producing methods
----------------------------------------

Most :class:`Dialog` methods that create a widget (actually: all methods that
supervise the exit of a widget) return a value which fits into one of these
categories:

  #. The return value is a :term:`Dialog exit code` (see below).

  #. The return value is a sequence whose first element is a Dialog exit code
     (the rest of the sequence being related to what the user entered in the
     widget).

For instance, :meth:`Dialog.yesno` returns a single Dialog exit code that will
typically be :attr:`Dialog.OK` or :attr:`Dialog.CANCEL`, depending on the
button chosen by the user. However, :meth:`Dialog.checklist` returns a tuple
of the form :samp:`({code}, [{tag}, ...])` whose first element is a Dialog
exit code and second element lists all tags for the entries selected by the
user.

.. _Dialog-exit-code:

"Dialog exit code" (high-level)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A :dfn:`Dialog exit code`, or :dfn:`high-level exit code`, is a string
indicating how/why a widget-producing method ended. Most widgets return one of
the :term:`standard Dialog exit codes <standard Dialog exit code>`: ``"ok"``,
``"cancel"``, ``"esc"``, ``"help"`` and ``"extra"``, respectively available as
:attr:`Dialog.OK`, :attr:`Dialog.CANCEL`, :attr:`Dialog.ESC`,
:attr:`Dialog.HELP` and :attr:`Dialog.EXTRA`, *i.e.,* attributes of the
:class:`Dialog` class. However, some widgets may return additional,
non-standard exit codes; for instance, the :meth:`~Dialog.inputmenu` widget
may return ``"accepted"`` or ``"renamed"`` in addition to the standard Dialog
exit codes.

When getting a Dialog exit code from a widget-producing method, user code
should compare it with :attr:`Dialog.OK` and friends (or equivalently, with
``"ok"`` and friends) using the ``==`` operator. This allows to easily replace
:attr:`Dialog.OK` and friends with objects that compare the same with ``"ok"``
and ``u"ok"`` in Python 2, for instance.

The following attributes of the :class:`Dialog` class hold the :term:`standard
Dialog exit codes <standard Dialog exit code>`:

.. autoattribute:: Dialog.OK

.. autoattribute:: Dialog.CANCEL

.. autoattribute:: Dialog.ESC

.. autoattribute:: Dialog.EXTRA

.. autoattribute:: Dialog.HELP

The following attributes are obsolete and should not be used in pythondialog
3.0 and later:

.. autoattribute:: Dialog.DIALOG_OK

.. autoattribute:: Dialog.DIALOG_CANCEL

.. autoattribute:: Dialog.DIALOG_ESC

.. autoattribute:: Dialog.DIALOG_EXTRA

.. autoattribute:: Dialog.DIALOG_HELP

.. autoattribute:: Dialog.DIALOG_ITEM_HELP

.. _dialog-exit-status:

"dialog exit status" (low-level)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When returning from a widget call, the :term:`Dialog exit code` is normally
derived by pythondialog from an integer called :dfn:`dialog exit status`, or
:dfn:`low-level exit code`. This integer is returned by the :program:`dialog`
backend upon exit. The different possible values for the dialog exit status
are referred to as ``DIALOG_OK``, ``DIALOG_CANCEL``, ``DIALOG_ESC``,
``DIALOG_ERROR``, ``DIALOG_EXTRA``, ``DIALOG_HELP`` and ``DIALOG_ITEM_HELP``
in the :manpage:`dialog(1)` manual page.

.. note::

  - ``DIALOG_HELP`` and ``DIALOG_ITEM_HELP`` both map to :attr:`Dialog.HELP`
    in pythondialog, because they both correspond to the same user action and
    the difference brings no information that the caller does not already
    have;

  - ``DIALOG_ERROR`` has no counterpart as a :class:`Dialog` attribute,
    because it is automatically translated into a :exc:`DialogError` exception
    when received.

In pythondialog 2.x, the low-level exit codes were available as the
``DIALOG_OK``, ``DIALOG_CANCEL``, etc. attributes of :class:`Dialog`
instances. For compatibility, the :class:`Dialog` class has attributes of the
same names that are mapped to :attr:`Dialog.OK`, :attr:`Dialog.CANCEL`, etc.,
but their use is deprecated as of pythondialog 3.0.


Adding an Extra button
----------------------

With most widgets, it is possible to add a supplementary button called
:dfn:`Extra button`. To do that, you simply have to use ``extra_button=True``
(keyword argument) in the widget call. By default, the button text is "Extra",
but you can specify another string with the *extra_label* keyword argument.

When the widget exits, you know if the :guilabel:`Extra` button was pressed if
the :term:`Dialog exit code` is :attr:`Dialog.EXTRA` (``"extra"``). Normally,
the rest of the return value is the same as if the widget had been closed with
:guilabel:`OK`. Therefore, if the widget normally returns a list of three
integers, for instance, you can expect to get the same information if
:guilabel:`Extra` is pressed instead of :guilabel:`OK`.

.. note::

  This feature can be particularly useful in combination with the *yes_label*,
  *no_label*, *help_button* and *help_label* :term:`common options <dialog
  common options>` to provide a completely different set of buttons than the
  default for a given widget.


Providing on-line help facilities
---------------------------------

With most :program:`dialog` widgets, it is possible to provide online help to
the final user. At the time of this writing (October 2014), there are three
main options governing these help facilities in the :program:`dialog` backend:
:option:`--help-button`, :option:`--item-help` and :option:`--help-status`.
Since :program:`dialog` 1.2-20130902, there is also :option:`--help-tags` that
modifies the way :option:`--item-help` works. As explained previously
(:ref:`passing-dialog-common-options`), in order to use these options in
pythondialog, you can pass the *help_button*, *item_help*, *help_status* and
*help_tags* keyword arguments to :class:`Dialog` widget-producing methods.

Adding a :guilabel:`Help` button
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to provide a :guilabel:`Help` button in addition to the normal
buttons of a widget, you can pass ``help_button=True`` (keyword argument) to
the corresponding :class:`Dialog` method. For instance, if *d* is a
:class:`Dialog` instance, you can write::

  code = d.yesno("<text>", height=10, width=40, help_button=True)

or::

  code, answer = d.inputbox("<text>", init="<init>",
                            help_button=True)

When the method returns, the :term:`Dialog exit code` is :attr:`Dialog.HELP`
(i.e., the string ``"help"``) if the user pressed the :guilabel:`Help` button.
Apart from that, it works exactly as if ``help_button=True`` had not been
used. In the last example, if the user presses the :guilabel:`Help` button,
*answer* will contain the user input, just as if :guilabel:`OK` had been
pressed. Similarly, if you write::

  code, t = d.checklist(
                "<text>", height=0, width=0, list_height=0,
                choices=[ ("Tag 1", "Item 1", False),
                          ("Tag 2", "Item 2", True),
                          ("Tag 3", "Item 3", True) ],
                help_button=True)

and find that ``code == Dialog.HELP``, then *t* contains the tag string for
the highlighted item when the :guilabel:`Help` button was pressed.

Finally, note that it is possible to choose the text written on the
:guilabel:`Help` button by supplying a string as the *help_label* keyword
argument.

.. _providing-inline-per-item-help:

Providing inline per-item help
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In addition to, or instead of the :guilabel:`Help` button, you can provide
:dfn:`item-specific help` that is normally displayed at the bottom of the
widget. This can be done by passing the ``item_help=True`` keyword argument to
the widget-producing method and by including the item-specific help strings in
the appropriate argument.

For widgets where item-specific help makes sense (i.e., there are several
elements that can be highlighted), there is usually a parameter, often called
*elements*, *choices*, *nodes*..., that must be provided as an iterable
describing the various lines/items/nodes/... that can be highlighted in the
widget. When ``item_help=True`` is passed, every element of this iterable must
be completed with a string which is the :dfn:`item-help string` of the element
(using :manpage:`dialog(1)` terminology). For instance, the following call
with no inline per-item help support::

  code, t = d.checklist(
                "<text>", height=0, width=0, list_height=0,
                choices=[ ("Tag 1", "Item 1", False),
                          ("Tag 2", "Item 2", True),
                          ("Tag 3", "Item 3", True) ],
                help_button=True)

can be altered this way to provide inline item-specific help::

  code, t = d.checklist(
                "<text>", height=0, width=0, list_height=0,
                choices=[ ("Tag 1", "Item 1", False, "Help 1"),
                          ("Tag 2", "Item 2", True,  "Help 2"),
                          ("Tag 3", "Item 3", True,  "Help 3") ],
                help_button=True, item_help=True, help_tags=True)

With this modification, the item-help string for the highlighted item is
displayed in the bottom line of the screen and updated as the user highlights
other items.

If you don't want a :guilabel:`Help` button, just use ``item_help=True``
without ``help_button=True`` (*help_tags* doesn't matter in this case). Then,
you have the inline help at the bottom of the screen, and the following
discussion about the return value can be ignored.

If the user chooses the :guilabel:`Help` button, *code* will be equal to
:attr:`Dialog.HELP` (``"help"``) and *t* will contain the tag string
corresponding to the highlighted item when the :guilabel:`Help` button was
pressed (``"Tag 1/2/3"`` in the example). This is because of the *help_tags*
option; without it (or with ``help_tags=False``), *t* would have contained the
:term:`item-help string` of the highlighted choice (``"Help 1/2/3"`` in the
example).

If you remember what was said earlier, if ``item_help=True`` had not been used
in the previous example, *t* would still contain the tag of the highlighted
choice if the user closed the widget with the :guilabel:`Help` button. This is
the same as when using ``item_help=True`` in combination with
``help_tags=True``; however, you would get the :term:`item-help string`
instead if *help_tags* were ``False`` (which is the default, as in the
:program:`dialog` backend, and in order to preserve compatibility with the
:meth:`Dialog.menu` implementation that is several years old).

Therefore, I recommend for consistency to use ``help_tags=True`` whenever
possible when specifying ``item_help=True``. This makes ``"--help-tags"`` a
good candidate for use with :meth:`Dialog.add_persistent_args` to avoid
repeating it over and over. However, there are two cases where
``help_tags=True`` cannot be used:

  - when the version of the :program:`dialog` backend is lower than
    1.2-20130902 (the :option:`--help-tags` option was added in this version);
  - when using empty or otherwise identical tags for presentation purposes
    (unless you don't need to tell which element was highlighted when the
    :guilabel:`Help` button was pressed, in which case it doesn't matter to be
    unable to discriminate between the tags).

Getting the widget status before the :guilabel:`Help` button was pressed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Typically, when the user chooses :guilabel:`Help` in a widget, the application
will display a dialog box such as :meth:`~Dialog.textbox`,
:meth:`~Dialog.msgbox` or :meth:`~Dialog.scrollbox` and redisplay the original
widget afterwards. For simple widgets such as :meth:`~Dialog.inputbox`, when
the :term:`Dialog exit code` is equal to :attr:`Dialog.HELP`, the return value
contains enough information to redisplay the widget in the same state it had
when :guilabel:`Help` was chosen. However, for more complex widgets such as
:meth:`~Dialog.radiolist` (resp. :meth:`~Dialog.checklist`, or
:meth:`~Dialog.form` and its derivatives), knowing the highlighted item is not
enough to restore the widget state after processing the help request: one
needs to know the checked item (resp. list of checked items, or form contents).

This is where the *help_status* keyword argument becomes useful. Example::

  code, t = d.checklist(
                "<text>", height=0, width=0, list_height=0,
                choices=[ ("Tag 1", "Item 1", False),
                          ("Tag 2", "Item 2", True),
                          ("Tag 3", "Item 3", True) ],
                help_button=True, help_status=True)

When :guilabel:`Help` is chosen, ``code == Dialog.HELP`` and *t* is a tuple of
the form :samp:`({tag}, {selected_tags}, {choices})` where:

  - *tag* gives the tag string of the highlighted item (which would be the
    value of *t* if *help_status* were set to ``False``);
  - *selected_tags* is the... list of selected tags (note that highlighting
    and selecting an item are different things!);
  - *choices* is a list built from the original *choices* argument of the
    :meth:`~Dialog.checklist` call and from the list of selected tags, that
    can be used as is to create a widget with the same items and selection
    state as the original widget had when :guilabel:`Help` was chosen.

Normally, pythondialog should always provide something similar to the last
item in the previous example in order to make it as easy as possible to
redisplay the widget in the appropriate state. To know precisely what is
returned with ``help_status=True``, the best way is probably to experiment
and/or read the code (by the way, there are many examples of widgets with
various combinations of the *help_button*, *item_help* and *help_status*
keyword arguments in the demo).

.. note::

  The various options related to help support are not mutually exclusive; they
  may be used together to provide good help support.

It is also worth noting that the documentation of the various widget-producing
methods is written, in most cases, under the assumption that the widget was
closed "normally" (typically, with the :guilabel:`OK` or :guilabel:`Extra`
button). For instance, a widget documentation may state that the method
returns a tuple of the form :samp:`({code}, {tag})` where *tag* is ..., but
actually, if using ``item_help=True`` with ``help_tags=False``, the *tag* may
very well be an :term:`item-help string`, and if using ``help_status=True``,
it is likely to be a structured object such as a tuple or list. Of course,
handling all these possible variations for all widgets would be a tedious task
and would probably significantly degrade the readability of said
documentation.

.. versionadded:: 3.0
   Proper support for the *item_help* and *help_status* common options.


Screen-related methods
----------------------

Getting the terminal size:

.. automethod:: Dialog.maxsize

.. automethod:: Dialog.set_background_title

Obsolete methods
^^^^^^^^^^^^^^^^

.. automethod:: Dialog.setBackgroundTitle

.. automethod:: Dialog.clear


Checking the versions of pythondialog and its backend
-----------------------------------------------------

Version of pythondialog
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: VersionInfo
   :members:
   :special-members:

.. autodata:: version_info
   :annotation:

.. autodata:: __version__
   :annotation:


Version of the backend
^^^^^^^^^^^^^^^^^^^^^^

The :class:`Dialog` constructor retrieves the version string of the
:program:`dialog` backend and stores it as an instance of a
:class:`BackendVersion` subclass into the
:attr:`Dialog.cached_backend_version` attribute. This allows doing things such
as (*d* being a :class:`Dialog` instance)::

  if d.compat == "dialog" and \
    d.cached_backend_version >= DialogBackendVersion("1.2-20130902"):
      ...

in a reliable way, allowing to fix the parsing and comparison algorithms right
in the appropriate :class:`BackendVersion` subclass, should the
:program:`dialog`-like backend versioning scheme change in unforeseen ways.

As :program:`Xdialog` seems to be dead and not to support
:option:`--print-version`, the :attr:`Dialog.cached_backend_version` attribute
is set to ``None`` in :program:`Xdialog`-compatibility mode (2013-09-12).
Should this ever change, one should define an :class:`XDialogBackendVersion`
class to handle the particularities of the :program:`Xdialog` versioning
scheme.

.. attribute:: Dialog.cached_backend_version

  Instance of a :class:`BackendVersion` subclass; it is initialized by the
  :class:`Dialog` constructor and used to store the backend version, avoiding
  the need to repeatedly call ``dialog --print-version`` or a similar
  command, depending on the backend.

  When using the :program:`dialog` backend,
  :attr:`Dialog.cached_backend_version` is a :class:`DialogBackendVersion`
  instance.

.. automethod:: Dialog.backend_version


Enabling debug facilities
-------------------------

.. automethod:: Dialog.setup_debug


Miscellaneous methods
---------------------

.. automethod:: Dialog.add_persistent_args

.. note::

   When :meth:`Dialog.__init__` is called with
   :samp:`{pass_args_via_file}=True` (or without any explicit setting for this
   option, and the pythondialog as well as :program:`dialog` versions are
   recent enough so that the option is enabled by default), then the arguments
   are not directly passed to :program:`dialog`. Instead, all arguments are
   written to a temporary file which :program:`dialog` is pointed to via
   :option:`--file`. This ensures better confidentiality with respect to other
   users of the same computer.

.. automethod:: Dialog.dash_escape

.. automethod:: Dialog.dash_escape_nf

.. _examples-of-dash-escaping:

A contrived example using these methods could be the following, which sets a
weird background title starting with two dashes (``--My little program``) for
the life duration of a :class:`Dialog` instance *d*::

  d.add_persistent_args(d.dash_escape_nf(
      ["--backtitle", "--My little program"]))

or, equivalently::

  d.add_persistent_args(["--backtitle"]
      + d.dash_escape(["--My little program"]))
