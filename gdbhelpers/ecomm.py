# ecomm

import gdb
import tempfile
import os

class EComm(gdb.Command):
    """Edit commands for a breakpoint and re-apply."""

    def __init__(self):
        super(EComm, self).__init__("ecomm", gdb.COMMAND_BREAKPOINTS,
                                    gdb.COMPLETE_NONE)

    def twrite(self, filename, bp):
        with open(filename, 'w') as f:
            f.write('# Edit the commands, save, and exit the editor.\n')
            f.write('# You can simply clear the whole file to have no changes take effect.\n')
            f.write('commands ' + str(bp.number) + '\n')
            f.write(bp.commands)
            f.write('end\n')

    def edit(self, filename):
        ed = os.getenv("BLOCKING_EDITOR")
        if ed is None:
            ed = os.getenv("EDITOR")
        os.system(ed + " " + filename)

    def reapply(self, filename):
        gdb.execute('source ' + filename)

    def edit_and_reapply(self, bp):
        fd, filename = tempfile.mkstemp()
        try:
            self.twrite(filename, bp)
            self.edit(filename)
            self.reapply(filename)
        finally:
            os.close(fd)
            os.remove(filename)

    def invoke(self, arg, from_tty):
        arg = int(arg)
        for bp in gdb.breakpoints():
            if bp.number == arg:
                self.edit_and_reapply(bp)
                return
        raise gdb.GdbError("breakpoint " + arg + " not found")

EComm()
