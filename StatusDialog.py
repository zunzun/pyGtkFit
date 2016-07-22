import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))


class StatusWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_type_hint(Gtk.WindowType.TOPLEVEL)
        self.set_size_request(400, 300) # minimum screen size
        self.set_position(Gtk.WindowPosition.CENTER)
        
        grid = Gtk.Grid()
        self.add(grid)
        
        self.textView = Gtk.TextView()
        
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(self.textView)   
        scrolledTextWindow.set_hexpand(True)
        scrolledTextWindow.set_vexpand(True)
        grid.attach(scrolledTextWindow, 0, 0, 1, 1)
        
        self.show_all()
        
