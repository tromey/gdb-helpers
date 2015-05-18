## Overview

This adds some new commands and convenience functions to gdb.
I've found these useful while hacking on firefox.

Also, for Emacs users, this arranges to set `EDITOR` to `emacsclient -n`
when gdb is running inside Emacs, so that the `edit` command will contact
Emacs and not wait for the edit to be complete.  (In this case it also
sets another environment variable so the new `ecomm` command will do
the right thing.)

## Installing

The simplest way is to:

```
make hack-gdbinit
```

This will edit your `.gdbinit` to load the helpers.

## Oddball Features:

* If you put `\E` into your `extended-prompt`, then when running gdb
  in the shell, changes to the current location will be sent to a
  running Emacs using `emacsclient`.  For best results you will also
  want to `(setq server-raise-frame nil)` in Emacs.

  This is useful if you have to run gdb from the shell for some
  reason, and want see the sources, and don't want to use the TUI, and
  gdb-gui fails due to an obscure bug on your machine.  Cough cough.

## New commands:

* `ecomm N`.  Edit the commands for breakpoint N.  This writes the
  commands out to a file and pops up your editor.  When you're done
  the commands are re-applied.

* `hier CLASS`.  Print the class hierarchy of a class, one line per
  base class.

## New functions

* `$_python(STR)`.  Evaluate `STR` as a Python expression.  This is an
  occasionally handy shortcut to use in place of a new `gdb.Function`
  implementation.

* `$_typeof(EXP)`.  Evaluates EXP and then returns a string
  representation of its dynamic type.  This is handy in conjunction
  with `$_regex` (distributed with gdb) in breakpoint conditions --
  you can easily break only when a specific sub-class is seen.

* `$_upvar(NAME, LIMIT)`.  Search up for at most LIMIT frames, looking
  for a variable named NAME (which must be a string).  If such a
  variable is found, return its value.  Otherwise, an error results.

* `$_up([N = 1])`.  Move up N frames and return 1.  This is sometimes
  useful in conjunction with `$_var`.

* `$_var(NAME)`.  Return the value of a variable named NAME in the
  current frame.
