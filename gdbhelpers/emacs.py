import gdb
import gdb.prompt
import os

_last_command = None

def emacs_updater(ignore):
    "Automatically update Emacs with the current location."
    # Don't bother if inside emacs.
    if not os.getenv("EMACS"):
        try:
            frame = gdb.selected_frame()
        except:
            frame = None
        if frame and frame.find_sal():
            sal = frame.find_sal()
            if sal.symtab and sal.symtab.filename and sal.line:
                global _last_command
                command = 'emacsclient -n +%d %s' % (sal.line,
                                                     sal.symtab.filename)
                if command is not _last_command:
                    _last_command = command
                    os.system(command)
    return ''

gdb.prompt.prompt_substitutions['E'] = emacs_updater
