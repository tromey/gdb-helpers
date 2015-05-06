all: load-helpers.py
	@:

load-helpers.py: load-helpers.py.in
	sed -e "s,HERE,`pwd`," < load-helpers.py.in > load-helpers.py

hack-gdbinit: all
	if test -f $$HOME/.gdbinit && `grep -q load-helpers $$HOME/.gdbinit`; then \
	  :; \
	else \
	  echo "source `pwd`/load-helpers.py" >> $$HOME/.gdbinit; \
	fi
