import gdb
import gdbhelpers
from gdb.FrameDecorator import FrameDecorator

_colors = ["none", "black", "red", "green", "yellow", "blue", "magenta",
           "cyan", "white"]

class _Prefix(gdb.Command):
    """Generic command for modifying backtrace color settings."""

    def __init__(self, setorshow, name):
        super(_Prefix, self).__init__(setorshow + " backtrace " + name,
                                      gdb.COMMAND_NONE, prefix = True)

_Prefix("set", "filename")
_Prefix("set", "function")
_Prefix("set", "argument")
_Prefix("show", "filename")
_Prefix("show", "function")
_Prefix("show", "argument")

class _ColorParameter(gdb.Parameter):
    def __init__(self, item, attribute, values):
        self.set_doc = "Set the %s %s" % (item, attribute)
        self.show_doc = "Show the %s %s" % (item, attribute)
        self.item = item
        self.attribute = attribute
        super(_ColorParameter, self).__init__("backtrace " + item + " "
                                              + attribute,
                                              gdb.COMMAND_NONE,
                                              gdb.PARAM_ENUM,
                                              values)
        self.value = values[0]

    def get_show_string(self, pvalue):
        return "The current %s %s is: %s" % (self.item, self.attribute,
                                             self.value)

    def get_set_string(self):
        return ""

class _Item(object):
    def __init__(self, name):
        self.bold = _ColorParameter(name, "intensity",
                                    ["normal", "bold", "faint"])
        self.foreground = _ColorParameter(name, "foreground", _colors)
        self.background = _ColorParameter(name, "background", _colors)

    def get_escape(self):
        result = []
        if self.bold.value == "bold":
            result.append("1")
        elif self.bold.value == "faint":
            result.append("2")
        if self.foreground.value != "none":
            result.append("3" + str(_colors.index(self.foreground.value) - 1))
        if self.background.value != "none":
            result.append("4" + str(_colors.index(self.background.value) - 1))
        if len(result) == 0:
            return None
        return "\x1b[" + ";".join(result) + "m"

filename_item = _Item("filename")
function_item = _Item("function")
arg_item = _Item("argument")

def colorize(item, text):
    if type(text) != str or gdbhelpers.in_emacs():
        return text
    esc = item.get_escape()
    if esc is None:
        return text
    return esc + str(text) + "\x1b[m"

class SymbolWrapper(object):
    def __init__(self, frame, symval):
        self.symval = symval
        self.frame = frame

    def value(self):
        value = self.symval.value()
        if value != None:
            return value
        sym = self.symval.symbol()
        return sym.value(self.frame)

    def symbol(self):
        sym = self.symval.symbol()
        if type(sym) == str:
            text = sym
        elif type(sym) == gdb.Symbol:
            text = sym.print_name
        else:
            return sym
        return colorize(arg_item, text)

class ColorDecorator(FrameDecorator):
    def __init__(self, fobj):
        super(ColorDecorator, self).__init__(fobj)
        self._fobj = fobj

    def function(self):
        return colorize(function_item, self._fobj.function())

    def filename(self):
        return colorize(filename_item, self._fobj.filename())

    def wrap_symbol(self, symval):
        return SymbolWrapper(self.inferior_frame(), symval)

    def frame_args(self):
        args = self._fobj.frame_args()
        if args is None:
            return None
        return map(self.wrap_symbol, args)

class ColorFilter(object):
    def __init__(self):
        self.name = "colorize"
        self.priority = 100
        self.enabled = True
        gdb.frame_filters[self.name] = self

    def filter(self, frame_iter):
        return map(ColorDecorator, frame_iter)

ColorFilter()

# Defaults.
gdb.execute("set backtrace argument foreground red", to_string = True)
gdb.execute("set backtrace function foreground blue", to_string = True)
gdb.execute("set backtrace function intensity bold", to_string = True)
gdb.execute("set backtrace filename foreground cyan", to_string = True)
