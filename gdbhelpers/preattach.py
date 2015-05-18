# preattach

import gdb
import os
import subprocess

class Preattach(gdb.Command):
    """ blah """

    def __init__(self):
        super(Preattach, self).__init__("preattach", gdb.COMMAND_RUNNING,
                                        gdb.COMPLETE_NONE)

    def invoke(self, arg, from_tty):
        script = os.path.join(os.path.dirname(__file__), 'preattach.stp')
        pid = subprocess.check_output(['stap', '-g', script, arg.strip()])
        gdb.execute('attach ' + pid.strip(), from_tty)

Preattach()
