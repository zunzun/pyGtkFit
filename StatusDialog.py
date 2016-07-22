import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))


class StatusWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self)

        self.textView = Gtk.TextView()
        self.add(self.textView)
        self.set_type_hint(Gtk.WindowType.TOPLEVEL)
        
        self.set_size_request(400, 300) # minimum screen size
        self.set_position(Gtk.WindowPosition.CENTER)