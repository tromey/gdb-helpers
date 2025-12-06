# gdbhelpers module

import os


def in_emacs():
    if os.getenv("INSIDE_EMACS"):
        return True
    return False


# These are cases where gdb's default ought to change.
import gdb

import gdbhelpers.ecomm
import gdbhelpers.editor
import gdbhelpers.emacs
import gdbhelpers.hierarchy
import gdbhelpers.preattach
import gdbhelpers.python
import gdbhelpers.tuistack
import gdbhelpers.typeof
import gdbhelpers.upvar

gdb.execute("set print pretty on")
gdb.execute("set print object on")
gdb.execute("set breakpoint pending on")
gdb.execute("set python print-stack full")
