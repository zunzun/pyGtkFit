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

        self.equationSelect_2D = 0
        self.equationSelect_3D = 0
        self.fittingTargetSelect_2D = 0
        self.fittingTargetSelect_3D = 0


        # Gtk grid layout
        grid = Gtk.Grid()
        self.add(grid)

        # ROW 0 - empty labels as visual buffers
        row, col = (0, 0) # left edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (0, 2) # center
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (0, 4) # right edge
        l = Gtk.Label("      ")
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
        self.textView_2D = Gtk.TextView()
        self.textView_2D.get_buffer().set_text(dfc.exampleText_2D) # inital text data
        self.textView_2D.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(self.textView_2D)   
        scrolledTextWindow.set_hexpand(True)
        scrolledTextWindow.set_vexpand(True)
        grid.attach(scrolledTextWindow, col, row, 1, 1) 

        row, col = (2, 3)
        self.textView_3D = Gtk.TextView()
        self.textView_3D.get_buffer().set_text(dfc.exampleText_3D) # inital text data
        self.textView_3D.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(self.textView_3D)   
        scrolledTextWindow.set_hexpand(True)
        scrolledTextWindow.set_vexpand(True)
        grid.attach(scrolledTextWindow, col, row, 1, 1) 

        # ROW 3 - empty labels as visual buffers
        row, col = (3, 0) # left edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (3, 2) # center
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (3, 4) # right edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)

        # ROW 4 - text data entry labels
        # no "self" needed as no later references exist
        row, col = (4, 1)
        l = Gtk.Label()
        l.set_markup("<b>--- Example 2D Equations ---</b>")
        grid.attach(l, col, row, 1, 1)

        row, col = (4, 3)
        l = Gtk.Label()
        l.set_markup("<b>--- Example 3D Equations ---</b>")
        grid.attach(l, col, row, 1, 1)


        # ROW 5 - equation selection radio buttons
        row, col = (5, 1)
        vbox = Gtk.VBox(False, 0)
        grid.attach(vbox, col, row, 1, 1)        
        rbgroup = None
        index=0
        for exampleEquationText in dfc.exampleEquationList_2D:
            rb = Gtk.RadioButton(group=rbgroup, label=exampleEquationText)
            rb.connect("toggled", self.OnEquationSelect_2D, index) # index is used as data in callback
            index += 1
            vbox.pack_start(rb, True, True, 0)
            if rbgroup == None:
                rb.set_active(True)
                rbgroup = rb
            else:
                rb.set_active(False)

        row, col = (5, 3)
        vbox = Gtk.VBox(False, 0)
        grid.attach(vbox, col, row, 1, 1)        
        rbgroup = None
        index=0
        for exampleEquationText in dfc.exampleEquationList_3D:
            rb = Gtk.RadioButton(group=rbgroup, label=exampleEquationText)
            rb.connect("toggled", self.OnEquationSelect_3D, index) # index is used as data in callback
            index += 1
            vbox.pack_start(rb, True, True, 0)
            if rbgroup == None:
                rb.set_active(True)
                rbgroup = rb
            else:
                rb.set_active(False)

        # ROW 6 - empty labels as visual buffers
        row, col = (6, 0) # left edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (6, 2) # center
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (6, 4) # right edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)

        # ROW 7 - fitting target selection labels
        # no "self" needed as no later references exist
        row, col = (7, 1)
        l = Gtk.Label()
        l.set_markup("<b>--- Fitting Target 2D ---</b>")
        grid.attach(l, col, row, 1, 1)

        row, col = (7, 3)
        l = Gtk.Label()
        l.set_markup("<b>--- Fitting Target 3D ---</b>")
        grid.attach(l, col, row, 1, 1)

        # ROW 8 - fitting target selection radio buttons
        row, col = (8, 1)
        vbox = Gtk.VBox(False, 0)
        grid.attach(vbox, col, row, 1, 1)        
        rbgroup = None
        index=0
        for fittingTargetText in dfc.fittingTargetList:
            rb = Gtk.RadioButton(group=rbgroup, label=fittingTargetText)
            rb.connect("toggled", self.OnFittingTargetSelect_2D, index) # index is used as data in callback
            index += 1
            vbox.pack_start(rb, True, True, 0)
            if rbgroup == None:
                rb.set_active(True)
                rbgroup = rb
            else:
                rb.set_active(False)

        row, col = (8, 3)
        vbox = Gtk.VBox(False, 0)
        grid.attach(vbox, col, row, 1, 1)        
        rbgroup = None
        index=0
        for fittingTargetText in dfc.fittingTargetList:
            rb = Gtk.RadioButton(group=rbgroup, label=fittingTargetText)
            rb.connect("toggled", self.OnFittingTargetSelect_3D, index) # index is used as data in callback
            index += 1
            vbox.pack_start(rb, True, True, 0)
            if rbgroup == None:
                rb.set_active(True)
                rbgroup = rb
            else:
                rb.set_active(False)

        # ROW 9 - empty labels as visual buffers
        row, col = (9, 0) # left edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (9, 2) # center
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (9, 4) # right edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)

        # ROW 10 - fitting buttons
        row, col = (10, 1)
        b = Gtk.Button(label = 'Fit 2D Text Data')
        b.connect("clicked", self.OnFit_2D, None)
        grid.attach(b, col, row, 1, 1)
    
        row, col = (10, 3)
        b = Gtk.Button(label = 'Fit 3D Text Data')
        b.connect("clicked", self.OnFit_3D, None)
        grid.attach(b, col, row, 1, 1)

        # ROW 11 - empty label as visual buffer
        row, col = (11, 0) # left edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (11, 2) # center
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)
        row, col = (11, 4) # right edge
        l = Gtk.Label("      ")
        grid.attach(l, col, row, 1, 1)


    def OnFit_2D(self, widget, data=None):
        print("2D Fit clicked")


    def OnFit_3D(self, widget, data=None):
        print("3D Fit clicked")


    def OnEquationSelect_2D(self, widget, data=None):
        if widget.get_active(): # only want toggle "on" item
            self.equationSelect_2D = data


    def OnEquationSelect_3D(self, widget, data=None):
        if widget.get_active(): # only want toggle "on" item
            self.equationSelect_3D = data


    def OnFittingTargetSelect_2D(self, widget, data=None):
        if widget.get_active(): # only want toggle "on" item
            self.fittingTargetSelect_2D = data


    def OnFittingTargetSelect_3D(self, widget, data=None):
        if widget.get_active(): # only want toggle "on" item
            self.fittingTargetSelect_3D = data



if __name__ == "__main__":
    win = FittingWindow()
    win.set_title("pyGtk - Curve And Surface Fitting Interface")

    win.set_size_request(800, 600) # minimum screen size
    win.set_position(1) # 1 = Gtk.WIN_POS_CENTER failed in development

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
