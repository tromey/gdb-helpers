# typeof

import gdb
from gdb.FrameIterator import FrameIterator

class Typeof(gdb.Function):
    """$_typeof - return the type of a value as a string.

Usage:
    $_typeof(EXP)
"""

    def __init__(self):
        super(Typeof, self).__init__('_typeof')

    def invoke(self, val):
        return str(val.dynamic_type)

Typeof()
