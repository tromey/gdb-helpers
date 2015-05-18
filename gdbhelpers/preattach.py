# preattach

import gdb
import os
import subprocess

class Preattach(gdb.Command):
    """Attach to the next instance of a program.
Usage:
    preattach BASENAME
This runs a SystemTap script that watches for the next time a program
that has the given basename is invoked.  Then, a SIGSTOP is delivered
to that process, and gdb attaches to it."""

    def __init__(self):
        super(Preattach, self).__init__("preattach", gdb.COMMAND_RUNNING,
                                        gdb.COMPLETE_NONE)

    def invoke(self, arg, from_tty):
        script = os.path.join(os.path.dirname(__file__), 'preattach.stp')
        pid = subprocess.check_output(['stap', '-g', script, arg.strip()])
        gdb.execute('attach ' + pid.strip(), from_tty)

Preattach()
