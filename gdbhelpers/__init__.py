# gdbhelpers module

import gdb

import gdbhelpers.ecomm
import gdbhelpers.editor
import gdbhelpers.emacs
import gdbhelpers.hierarchy
import gdbhelpers.preattach
import gdbhelpers.python
import gdbhelpers.tuistack
import gdbhelpers.typeof
import gdbhelpers.upvar  # noqa: F401

gdb.execute("set print pretty on")
gdb.execute("set print object on")
gdb.execute("set breakpoint pending on")
gdb.execute("set python print-stack full")
