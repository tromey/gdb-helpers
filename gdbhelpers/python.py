# $_python function.

import gdb

class Python(gdb.Function):
    """$_python - evaluate a Python expression

Usage:
    $_python(STR)

This function evaluates a Python expression and returns
the result to gdb.  STR is a string which is parsed and evalled."""

    def __init__(self):
        super(Python, self).__init__('_python')

    def invoke(self, expr):
        return eval(expr.string())

Python()
