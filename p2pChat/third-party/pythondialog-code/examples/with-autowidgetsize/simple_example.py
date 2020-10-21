#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# simple_example.py --- Short and straightforward example using pythondialog
# Copyright (C) 2013, 2014  Florent Rougon
#
# This program is in the public domain.

import sys, locale
from dialog import Dialog

# This is almost always a good thing to do at the beginning of your programs.
locale.setlocale(locale.LC_ALL, '')

# Initialize a dialog.Dialog instance
#
# With the 'autowidgetsize' option enabled, pythondialog's widget-producing
# methods behave as if width=0, height=0, etc. had been passed, except where
# these parameters are explicitely specified with different values.
d = Dialog(dialog="dialog", autowidgetsize=True)
d.set_background_title("A Simple Example")


# *****************************************************************************
# *                             'msgbox' example                              *
# *****************************************************************************
d.msgbox("""\
This is a very simple example of a program using pythondialog.

Contrary to what is done in demo.py, the Dialog exit code for the Escape key \
is not checked after every call, therefore it is not so easy to exit from \
this program as it is for the demo. The goal here is to show basic \
pythondialog usage in its simplest form.

With not too old versions of dialog, the size of dialog boxes is \
automatically computed when one passes width=0 and height=0 to the \
widget call. This is the method used here in most cases.""",
         title="'msgbox' example")


# *****************************************************************************
# *                              'yesno' example                              *
# *****************************************************************************

# The 'no_collapse=True' used in the following call tells dialog not to replace
# multiple contiguous spaces in the text string with a single space.
code = d.yesno("""\
The 'yesno' widget allows one to display a text with two buttons beneath, \
which by default are labelled "Yes" and "No".

The return value is not simply True or False: for consistency with \
dialog and the other widgets, the return code allows to distinguish \
between:

  OK/Yes      Dialog.OK         (equal to the string "ok")
  Cancel/No   Dialog.CANCEL     (equal to the string "cancel")
  <Escape>    Dialog.ESC        when the Escape key is pressed
  Help        Dialog.HELP       when help_button=True was passed and the
                                Help button is pressed (only for 'menu' in
                                pythondialog 2.x)
  Extra       Dialog.EXTRA      when extra_button=True was passed and the
                                Extra button is pressed

The DIALOG_ERROR exit status of dialog has no equivalent in this list, \
because pythondialog translates it into an exception.""",
               title="'yesno' example", no_collapse=True,
               help_button=True)

if code == d.OK:
    msg = "You chose the 'OK/Yes' button in the previous dialog."
elif code == d.CANCEL:
    msg = "You chose the 'Cancel/No' button in the previous dialog."
elif code == d.ESC:
    msg = "You pressed the Escape key in the previous dialog."
elif code == d.HELP:
    msg = "You chose the 'Help' button in the previous dialog."
else:
    msg = "Unexpected exit code from d.yesno(). Please report a bug."

# It is possible to explicitely specify the width and height of the widget
# instead of relying on 'autowidgetsize'.
d.msgbox(msg, width=50, height=7)


# *****************************************************************************
# *                            'inputbox' example                             *
# *****************************************************************************
code, user_input = d.inputbox("""\
The 'inputbox' widget can be used to read input (as a string) from the user. \
You can test it now:""",
                              init="Initial contents",
                              title="'inputbox' example",
                              help_button=True, extra_button=True,
                              extra_label="Cool button")

if code == d.OK:
    msg = "Your input in the previous dialog was '{0}'.".format(user_input)
elif code == d.CANCEL:
    msg = "You chose the 'Cancel' button in the previous dialog."
elif code == d.ESC:
    msg = "You pressed the Escape key in the previous dialog."
elif code == d.HELP:
    msg = "You chose the 'Help' button with input '{0}' in the previous " \
    "dialog.".format(user_input)
elif code == d.EXTRA:
    msg = 'You chose the Extra button ("Cool button") with input \'{0}\' ' \
    "in the previous dialog.".format(user_input)
else:
    msg = "Unexpected exit code from d.inputbox(). Please report a bug."

d.msgbox("{0}\n\nThis little sample program is now finished. Bye bye!".format(
        msg), title="Bye bye!")

sys.exit(0)
