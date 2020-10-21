.. currentmodule:: dialog

.. _widgets:

The :class:`Dialog` widgets
===========================

This section describes all widgets (or dialog boxes) offered by the
:class:`Dialog` class. The descriptions of many of them are adapted from the
:manpage:`dialog(1)` manual page, with the kind permission of `Thomas Dickey
<https://invisible-island.net/>`_.


.. note::

  All unqualified method names in this section are methods of the
  :class:`Dialog` class. In other words, whenever a method :meth:`!foo` is
  mentioned, you have to understand :meth:`!dialog.Dialog.foo`.

.. warning::

  Concerning the older widgets that have fixed defaults for the length
  parameters such as *width* and *height*:

  Even though explicitely setting one of these length parameters to ``None``
  will not cause any error in this version, please don't do it. If you know
  the size you want, specify it directly (e.g., ``width=78``). On the other
  hand, if you want :program:`dialog` to automagically figure out a suitable
  size, you have two options:

    - either enable the :ref:`autowidgetsize <autowidgetsize>` option and
      make sure not to specify the length parameter in the widget call;
    - or explicitely set it to ``0`` (e.g., ``width=0``).


Displaying multi-line text
--------------------------

Message box
^^^^^^^^^^^

.. automethod:: Dialog.msgbox

.. figure:: screenshots/msgbox.png
   :align: center

   :meth:`~Dialog.msgbox` example


Text box
^^^^^^^^

.. automethod:: Dialog.textbox

.. figure:: screenshots/textbox.png
   :align: center

   :meth:`~Dialog.textbox` example


Scroll box
^^^^^^^^^^

.. Automethod:: Dialog.scrollbox

.. figure:: screenshots/scrollbox.png
   :align: center

   :meth:`~Dialog.scrollbox` example


Edit box
^^^^^^^^

.. automethod:: Dialog.editbox

.. figure:: screenshots/editbox.png
   :align: center

   :meth:`~Dialog.editbox` example

.. automethod:: Dialog.editbox_str


Progress box
^^^^^^^^^^^^

.. automethod:: Dialog.progressbox

.. figure:: screenshots/progressbox.png
   :align: center

   :meth:`~Dialog.progressbox` example


Program box
^^^^^^^^^^^

.. automethod:: Dialog.programbox

.. figure:: screenshots/programbox.png
   :align: center

   :meth:`~Dialog.programbox` example


Tail box
^^^^^^^^

.. automethod:: Dialog.tailbox

.. figure:: screenshots/tailbox.png
   :align: center

   :meth:`~Dialog.tailbox` example



Displaying transient messages
-----------------------------

Info box
^^^^^^^^

.. automethod:: Dialog.infobox

.. figure:: screenshots/infobox.png
   :align: center

   :meth:`~Dialog.infobox` example


Pause
^^^^^

.. automethod:: Dialog.pause

.. figure:: screenshots/pause.png
   :align: center

   :meth:`~Dialog.pause` example


Progress meters
---------------

.. _gauge-widget:

Regular gauge
^^^^^^^^^^^^^

.. automethod:: Dialog.gauge_start

.. automethod:: Dialog.gauge_update

.. automethod:: Dialog.gauge_iterate

.. automethod:: Dialog.gauge_stop

.. figure:: screenshots/gauge.png
   :align: center

   :meth:`~Dialog.gauge` example


Mixed gauge
^^^^^^^^^^^

.. automethod:: Dialog.mixedgauge

.. figure:: screenshots/mixedgauge.png
   :align: center

   :meth:`~Dialog.mixedgauge` example


List-like widgets
-----------------

Build list
^^^^^^^^^^

.. automethod:: Dialog.buildlist

.. figure:: screenshots/buildlist.png
   :align: center

   :meth:`~Dialog.buildlist` example


Check list
^^^^^^^^^^

.. automethod:: Dialog.checklist

.. figure:: screenshots/checklist.png
   :align: center

   :meth:`~Dialog.checklist` example


Menu
^^^^

.. automethod:: Dialog.menu

.. figure:: screenshots/menu.png
   :align: center

   :meth:`~Dialog.menu` example


Radio list
^^^^^^^^^^

.. automethod:: Dialog.radiolist

.. figure:: screenshots/radiolist.png
   :align: center

   :meth:`~Dialog.radiolist` example


Tree view
^^^^^^^^^

.. automethod:: Dialog.treeview

.. figure:: screenshots/treeview.png
   :align: center

   :meth:`~Dialog.treeview` example



Single-line input fields
------------------------

Input box
^^^^^^^^^

.. automethod:: Dialog.inputbox

.. figure:: screenshots/inputbox.png
   :align: center

   :meth:`~Dialog.inputbox` example


Input menu
^^^^^^^^^^

.. automethod:: Dialog.inputmenu

.. figure:: screenshots/inputmenu.png
   :align: center

   :meth:`~Dialog.inputmenu` example


Password box
^^^^^^^^^^^^

.. automethod:: Dialog.passwordbox

.. figure:: screenshots/passwordbox.png
   :align: center

   :meth:`~Dialog.passwordbox` example



Forms
-----

Form
^^^^

.. automethod:: Dialog.form

.. figure:: screenshots/form.png
   :align: center

   :meth:`~Dialog.form` example


Mixed form
^^^^^^^^^^

.. automethod:: Dialog.mixedform

.. figure:: screenshots/mixedform.png
   :align: center

   :meth:`~Dialog.mixedform` example


Password form
^^^^^^^^^^^^^

.. automethod:: Dialog.passwordform

.. figure:: screenshots/passwordform.png
   :align: center

   :meth:`~Dialog.passwordform` example


Selecting files and directories
-------------------------------

Directory selection
^^^^^^^^^^^^^^^^^^^

.. automethod:: Dialog.dselect

.. figure:: screenshots/dselect.png
   :align: center

   :meth:`~Dialog.dselect` example


File or directory selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Dialog.fselect

.. figure:: screenshots/fselect.png
   :align: center

   :meth:`~Dialog.fselect` example


Date and time
-------------

Calendar
^^^^^^^^

.. automethod:: Dialog.calendar

.. figure:: screenshots/calendar.png
   :align: center

   :meth:`~Dialog.calendar` example


Time box
^^^^^^^^

.. automethod:: Dialog.timebox

.. figure:: screenshots/timebox.png
   :align: center

   :meth:`~Dialog.timebox` example


Miscellaneous
-------------

Range box
^^^^^^^^^

.. automethod:: Dialog.rangebox

.. figure:: screenshots/rangebox.png
   :align: center

   :meth:`~Dialog.rangebox` example


Yes/No
^^^^^^

.. automethod:: Dialog.yesno

.. figure:: screenshots/yesno.png
   :align: center

   :meth:`~Dialog.yesno` example
