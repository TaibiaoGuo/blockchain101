#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# setup.py --- Setup script for pythondialog
# Copyright (c) 2002-2019  Florent Rougon
#
# This file is part of pythondialog.
#
# pythondialog is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# pythondialog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
# MA  02110-1301 USA.

import os, sys, subprocess, traceback
from setuptools import setup


PACKAGE = "pythondialog"
# This is OK because dialog.py has no dependency outside the standard library.
from dialog import __version__ as VERSION


def run_gitlog_to_changelog(after_this_commit, output=None):
    args = [ "gitlog-to-changelog", "--format=%s%n%n%b%n", "--",
             "{0}..".format(after_this_commit) ]
    try:
        subprocess.check_call(args, stdout=output)
    except os.error:
        print(traceback.format_exc(), file=sys.stderr)

        print("""\
Error (see above for a traceback): unable to run {prg}
================================================={underlining}
Maybe this program is not installed on your system. You can download it from:

  {url}

Note: if you have problems with the infamous shell+Perl crap in the first lines
of that file, you can replace it with a simple shebang line such as
"#! /usr/bin/perl".""".format(
   prg=args[0],
   underlining="=" * len(args[0]),
   url="https://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=blob_plain;"
       "f=build-aux/gitlog-to-changelog"), file=sys.stderr)
        sys.exit(1)


def generate_changelog(ch_name, write_to_stdout=False):
    print("Converting the Git log into ChangeLog format...", end=' ',
          file=sys.stderr)
    orig_ch_name = "{0}.init".format(ch_name)
    # Most recent commit in the file referenced by 'orig_ch_name' (normally,
    # ChangeLog.init)
    last_commit_in_ch_init = "b69a76b550d62fd5965a3e37957aa3fbc11e1a5f"

    if write_to_stdout:
        run_gitlog_to_changelog(last_commit_in_ch_init)

        with open(orig_ch_name, "r", encoding="utf-8") as orig_ch:
            # Make sure the output is encoded in UTF-8
            sys.stdout.buffer.write(("\n" + orig_ch.read()).encode("utf-8"))
    else:
        tmp_ch_name = "{0}.new".format(ch_name)

        try:
            with open(tmp_ch_name, "w", encoding="utf-8") as tmp_ch:
                run_gitlog_to_changelog(last_commit_in_ch_init, output=tmp_ch)

                with open(orig_ch_name, "r", encoding="utf-8") as orig_ch:
                    tmp_ch.write("\n" + orig_ch.read())

            os.rename(tmp_ch_name, ch_name)
        finally:
            if os.path.exists(tmp_ch_name):
                os.unlink(tmp_ch_name)

    print("done.", file=sys.stderr)


def main():
    ch_name = "ChangeLog"
    if os.path.isdir(".git"):
        generate_changelog(ch_name)
    elif not os.path.isfile(ch_name):
        msg = """\
There is no {cl!r} file here and it seems you are not operating from a
clone of the Git repository (no .git directory); therefore, it is impossible to
generate the {cl!r} file from the Git log. Aborting.""".format(cl=ch_name)
        sys.exit(msg)

    with open("README.rst", "r", encoding="utf-8") as f:
        long_description = f.read()

    setup(name=PACKAGE,
          version=VERSION,
          description="A Python interface to the UNIX dialog utility and "
          "mostly-compatible programs",
          # According to
          # <https://packaging.python.org/specifications/core-metadata/> and
          # the rendering on PyPI, it appears that only the original author can
          # be listed in 'author'. See the AUTHORS file for other contributors.
          author="Robb Shecter",
          author_email="robb@acm.org",
          maintainer="Florent Rougon",
          maintainer_email="f.rougon@free.fr",
          url="http://pythondialog.sourceforge.net/",
          project_urls={
            "Documentation": "http://pythondialog.sourceforge.net/doc/",
            "SourceForge project page":
              "https://sourceforge.net/projects/pythondialog",
            "Git repository": "https://sourceforge.net/p/pythondialog/code/",
            "Mailing list": "https://sourceforge.net/p/pythondialog/mailman/",
            "Issue tracker":
              "https://sourceforge.net/p/pythondialog/_list/tickets",
          },
          long_description=long_description,
          long_description_content_type="text/x-rst",
          keywords="dialog,ncurses,Xdialog,text-mode interface,terminal",
          # Well, there isn't much UNIX-specific code in dialog.py, if at all.
          # I am putting Unix here only because of the dialog dependency...
          # Note: using the "Unix" case instead of "UNIX", because it is
          # spelled this way in Trove classifiers. This argument should be
          # unneeded given the Trove classifers, however omitting it leads to
          # an ugly 'Platform: UNKNOWN' in pythondialog.egg-info/PKG-INFO.
          platforms=["Unix"],
          classifiers=[
            "Programming Language :: Python :: 3",
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console :: Curses",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Library or Lesser General Public "
            "License (LGPL)",
            "Operating System :: Unix",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: User Interfaces",
            "Topic :: Software Development :: Widget Sets"],
          py_modules=["dialog"],
          python_requires=">=3")

if __name__ == "__main__": main()
