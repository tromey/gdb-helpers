# hierarchy

import gdb

class Hierarchy(gdb.Command):
    """Show the inheritance hierarchy of a class."""

    def __init__(self):
        super(Hierarchy, self).__init__("hierarchy", gdb.COMMAND_NONE,
                                        gdb.COMPLETE_SYMBOL)

    def print_hierarchy(self, typeobj, depth):
        print(' ' * depth)
        print(typeobj.name)
        typeobj = typeobj.strip_typedefs()
        for field in typeobj.fields():
            if not field.is_base_class:
                continue
            self.print_hierarchy(field.type, depth + 2)

    def invoke(self, arg, from_tty):
        typeobj = gdb.lookup_type(arg)
        self.print_hierarchy(typeobj, 0)

Hierarchy()
