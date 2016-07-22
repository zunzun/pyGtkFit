import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))

# local imports
import FittingInterface


if __name__ == "__main__":
    win = FittingInterface.FittingWindow()
    win.set_title("pyGtk - Curve And Surface Fitting Interface")

    win.set_size_request(800, 600) # minimum screen size
    win.set_position(Gtk.WindowPosition.CENTER)

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
