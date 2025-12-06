import os

import gdb
from gdb.frames import frame_iterator


def style(name, text):
    if hasattr(gdb, Style):
        return gdb.Style(name).apply(text)
    return text


class _TuiStack:
    def __init__(self, win):
        self._win = win
        win.title = "Stack"
        self._start = 0
        self._newest = None
        self._selected = None
        # A thread that cannot possibly match.
        self._thread = 23
        self._height = -1
        gdb.events.before_prompt.connect(self.render)
        self.render()

    def close(self):
        gdb.events.before_prompt.disconnect(self.render)

    def _get_frames(self, newest):
        if newest is None:
            # If there isn't a frame, just return an empty iterable.
            return ()
        return frame_iterator(newest, self._start, -1)

    def render(self):
        try:
            newest = gdb.newest_frame()
            selected = gdb.selected_frame()
        except gdb.error:
            newest = None
            selected = None

        if (
            self._newest == newest
            and self._selected == selected
            and self._thread == gdb.selected_thread()
            and self._height == self._win.height
        ):
            return
        self._newest = newest
        self._selected = selected
        self._thread = gdb.selected_thread()
        self._height = self._win.height

        line_count = 0
        output = ""
        for frame in self._get_frames(newest):
            # Check at the top, for the weird case where the window
            # height is 0.
            if line_count == self._win.height:
                break

            # Position arrow.
            iframe = frame.inferior_frame()
            if iframe == selected:
                output += "⇒ "
            else:
                output += "  "
            output += " #" + str(iframe.level()) + " "

            fn = frame.function()
            if fn is not None:
                output += style("function", fn)

            fname = frame.filename()
            lno = frame.line()
            if fname is not None and lno is not None:
                output += " at "
                output += style("filename", os.path.basename(fname))
                output += ":" + str(lno)

            output += "\n"
            line_count += 1

        self._win.write(output, full_window=True)

    def vscroll(self, num):
        save = self._start
        self._start += num
        if self._start < 0:
            self._start = 0
        if save != self._start:
            # Force a re-render, at least if there's a thread.
            self._thread = None
            self.render()


gdb.register_window_type("stack", _TuiStack)

gdb.execute("tui new-layout stack {-horizontal src 1 stack 1} 2 status 0 cmd 1")
