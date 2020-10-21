#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C)  2014 Florent Rougon
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Florent Rougon nor the names of other
#       contributors to this file may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL FLORENT ROUGON BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import locale
import time

from dialog import Dialog

# This is almost always a good thing to do at the beginning of your programs.
locale.setlocale(locale.LC_ALL, '')

d = Dialog(dialog="dialog")

button_names = {d.OK:     "OK",
                d.CANCEL: "Cancel",
                d.HELP:   "Help",
                d.EXTRA:  "Extra"}

code, tag = d.menu("Some text that will be displayed above the menu entries",
                   choices=[("Tag 1", "Item text 1"),
                            ("Tag 2", "Item text 2"),
                            ("Tag 3", "Item text 3")])

if code == d.ESC:
    d.msgbox("You got out of the menu by pressing the Escape key.")
else:
    text = "You got out of the menu by choosing the {} button".format(
        button_names[code])

    if code != d.CANCEL:
        text += ", and the highlighted entry at that time had tag {!r}".format(
        tag)

    d.msgbox(text + ".", width=40, height=10)

d.infobox("Bye bye...", width=0, height=0, title="This is the end")
time.sleep(2)

sys.exit(0)
