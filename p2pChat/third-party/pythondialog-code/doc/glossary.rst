.. _glossary:

Glossary
========

.. currentmodule:: dialog

.. glossary::

   dash escaping
      In a :program:`dialog` argument list, :dfn:`dash escaping` consists in
      prepending an element composed of two ASCII hyphens, i.e., the string
      ``'--'``, before every element that starts with two ASCII hyphens
      (``--``).

      Every :program:`dialog` option starts with ``--`` (e.g.,
      :option:`--yesno`), but there are valid cases where one needs to pass
      arguments to :program:`dialog` that start with ``--`` without having
      :program:`dialog` interpret them as options. For instance, one may want
      to print a text or label that starts with ``--``. In such a case, in
      order to avoid confusing the argument with a :program:`dialog` option,
      one must prepend an argument consisting solely of two ASCII hyphens
      (``--``). This is what is called *dash escaping* here.

      For instance, in order to display a message box containing the text
      ``--Not an option`` using POSIX shell syntax (the double quotes ``"``
      are stripped by the shell, :program:`dialog` does not see them):

      .. code-block:: sh

         dialog --msgbox -- "--Not an option" 0 0   # correct

         dialog --msgbox    "--Not an option" 0 0   # incorrect

      .. note::

         In pythondialog, most :class:`Dialog` public methods
         (:meth:`~Dialog.msgbox`, :meth:`~Dialog.yesno`, :meth:`~Dialog.menu`,
         etc.) know that the arguments they receive are not to be used as
         :program:`dialog` options, and therefore automatically perform dash
         escaping whenever needed to avoid having :program:`dialog` treat them
         as options. At the time of this writing, the only public method that
         requires you to be careful about leading double-dashes is the
         low-level :meth:`Dialog.add_persistent_args`, because it directly
         passes all its arguments to :program:`dialog` and cannot reliably
         guess which of these the user wants to be treated as
         :program:`dialog` options and which they want to be treated as
         *arguments* to a :program:`dialog` option.

      See these :ref:`examples of dash escaping in pythondialog
      <examples-of-dash-escaping>` using :meth:`Dialog.dash_escape` and
      :meth:`Dialog.dash_escape_nf`.

   Dialog exit code
   high-level exit code
      A :dfn:`Dialog exit code`, or :dfn:`high-level exit code`, is a string
      indicating how/why a widget-producing method ended. Most widgets return
      one of the :term:`standard Dialog exit codes <standard Dialog exit
      code>` (e.g., ``"ok"``, available as :attr:`Dialog.OK`). However, some
      widgets may return additional, non-standard exit codes; for instance,
      the :meth:`~Dialog.inputmenu` widget may return ``"accepted"`` or
      ``"renamed"`` in addition to the standard Dialog exit codes.

      When returning from a widget call, the Dialog exit code is normally
      derived from the :term:`dialog exit status`, also known as
      :term:`low-level exit code`.

      See :ref:`Dialog-exit-code` for more details.

   standard Dialog exit code
      A :dfn:`standard Dialog exit code` is a particular :term:`Dialog exit
      code`. Namely, it is one of the following strings: ``"ok"``,
      ``"cancel"``, ``"esc"``, ``"help"`` and ``"extra"``, respectively
      available as :attr:`Dialog.OK`, :attr:`Dialog.CANCEL`,
      :attr:`Dialog.ESC`, :attr:`Dialog.HELP` and :attr:`Dialog.EXTRA`,
      *i.e.,* attributes of the :class:`Dialog` class.

   dialog exit status
   low-level exit code
      The :dfn:`dialog exit status`, or :dfn:`low-level exit code`, is an
      integer returned by the :program:`dialog` backend upon exit, whose
      different possible values are referred to as ``DIALOG_OK``,
      ``DIALOG_CANCEL``, ``DIALOG_ESC``, ``DIALOG_ERROR``, ``DIALOG_EXTRA``,
      ``DIALOG_HELP`` and ``DIALOG_ITEM_HELP`` in the :manpage:`dialog(1)`
      manual page.

      See :ref:`dialog-exit-status` for more details.

   dialog common options
      Options that may be passed to many widgets using keyword arguments, for
      instance *defaultno*, *yes_label*, *extra_button* or
      *visit_items*. These options roughly correspond to those listed in
      :manpage:`dialog(1)` under the *Common Options* section.

      See :ref:`passing-dialog-common-options` for more details.

   item-help string
      When using ``item_help=True`` in a widget-producing method call, every
      item must have an associated string, called its :dfn:`item-help string`,
      that is normally displayed by :program:`dialog` at the bottom of the
      screen whenever the item is highlighted.

      See :ref:`providing-inline-per-item-help` for more details.
