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
import gdbhelpers.colorize
