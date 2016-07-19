import pickle
import pyeq3
import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))

# local imports
import DataForControls as dfc
import FittingThread


class FittingWindow(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self)

        # Gtk grid layout
        grid = Gtk.Grid()
        self.add(grid)

        # ROW 0 - empty labels as visual buffers
        row, col = (0, 0) # left edge
        l = Gtk.Label("   ")
        grid.attach(l, col, row, 1, 1)
        row, col = (0, 2) # center
        l = Gtk.Label("   ")
        grid.attach(l, col, row, 1, 1)
        row, col = (0, 4) # right edge
        l = Gtk.Label("   ")
        grid.attach(l, col, row, 1, 1)

        # ROW 1 - text data entry labels
        # no "self" needed as no later references exist
        row, col = (1, 1)
        l = Gtk.Label()
        l.set_markup("<b>--- 2D Data Text Editor ---</b>")
        grid.attach(l, col, row, 1, 1)

        row, col = (1, 3)
        l = Gtk.Label()
        l.set_markup("<b>--- 3D Data Text Editor ---</b>")
        grid.attach(l, col, row, 1, 1)

        # ROW 2 - text data input, no line wrap
        row, col = (2, 1)
        textView = Gtk.TextView()
        textView.get_buffer().set_text(dfc.exampleText_2D) # inital text data
        textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(textView)   
        grid.attach(scrolledTextWindow, col, row, 1, 1) 

        row, col = (2, 3)
        textView = Gtk.TextView()
        textView.get_buffer().set_text(dfc.exampleText_3D) # inital text data
        textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(textView)   
        grid.attach(scrolledTextWindow, col, row, 1, 1) 



if __name__ == "__main__":
    win = FittingWindow()
    win.set_title("pyGtk - Curve And Surface Fitting Interface")

    win.set_size_request(800, 600) # minimum screen size

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
