import gdb
import os

if os.getenv("INSIDE_EMACS"):
    # The blocking behavior of "edit" doesn't seem too useful,
    # especially when running inside Emacs, so this just disables it.
    # See the "ecomm" command though.
    os.putenv("EDITOR", "emacsclient -n")
    os.putenv("BLOCKING_EDITOR", "emacsclient")
    # At some point this stopped working automatically.
    # Maybe because Emacs switched back to --fullname?
    gdb.execute('set pagination off', to_string = True)
