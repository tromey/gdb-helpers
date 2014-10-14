import os

if os.getenv("EMACS"):
    # The blocking behavior of "edit" doesn't seem too useful,
    # especially when running inside Emacs, so this just disables it.
    # See the "ecomm" command though.
    os.putenv("EDITOR", "emacsclient -n")
    os.putenv("BLOCKING_EDITOR", "emacsclient")
