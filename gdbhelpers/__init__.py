# gdbhelpers module

import os

def in_emacs():
    if os.getenv("INSIDE_EMACS"):
        return True
    return False

import gdbhelpers.editor
import gdbhelpers.upvar
import gdbhelpers.typeof
import gdbhelpers.hierarchy
import gdbhelpers.ecomm
import gdbhelpers.preattach
import gdbhelpers.python
import gdbhelpers.emacs

# These are cases where gdb's default ought to change.
import gdb
gdb.execute("set print pretty on")
gdb.execute("set print object on")
gdb.execute("set breakpoint pending on")
gdb.execute("set python print-stack full")
