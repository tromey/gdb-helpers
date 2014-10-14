# upvar and up

import gdb
from gdb.FrameIterator import FrameIterator

# This is faster than gdb.lookup_symbol.
def find_var(frame, name):
    block = frame.block()
    while True:
        for sym in block:
            if sym.name == name:
                return sym.value(frame)
        if block.function:
            return None
        block = block.superblock

class Upvar(gdb.Function):
    """$_upvar - find a variable somewhere up the stack

Usage:
    $_upvar(NAME, LIMIT)

This function searches up the stack for a variable.
NAME is a string, the name of the variable to look for.
Starting with the selected frame, each stack frame is searched
for NAME.  If it is found, its value is returned.

If NAME is not found, an error is raised.

LIMIT is a number that limits the number of stack frames searched.
If LIMIT is reached, the number 0 is returned.
"""

    def __init__(self):
        super(Upvar, self).__init__('_upvar')

    def invoke(self, name,  limit):
        name = str(name)
        for frame in FrameIterator(gdb.selected_frame()):
            if limit <= 0:
                return gdb.Value(0)
            limit = limit - 1
            val = find_var(frame, name)
            if val is not None:
                return val
            raise gdb.GdbError("couldn't find %s" % name)


class Up(gdb.Function):
    """$_up - move up the stack

Usage:
    $_up(N [ = 1])

Like 'up', but suitable for use in an expression.
The argument says how many frames to move 'up'.

Always returns 1."""

    def __init__(self):
        super(Up, self).__init__('_up')

    def invoke(self, n = 1):
        for frame in FrameIterator(gdb.selected_frame()):
            if n <= 0:
                frame.select()
                break
            n = n - 1
        return 1


class Var(gdb.Function):
    """$_var - fetch a variable

Usage:
    $_var(NAME)

Return the value of the variable named NAME in the selected frame.
This is generally most useful in conjunction with $_up."""

    def __init__(self):
        super(Var, self).__init__('_var')

    def invoke(self, name):
        val = find_var(gdb.selected_frame(), name)
        if val is not None:
            return val
        raise gdb.GdbError("couldn't find %s" % name)

Upvar()
Up()
Var()
