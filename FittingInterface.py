import os, sys, time, pickle, queue
import pyeq3
import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGtk version is less than 3.0, please upgrade'))

# for custom signal
from gi.repository import GObject

# local imports
import DataForControls as dfc
import FittingThread
import StatusDialog


class FittingWindow(Gtk.Window):

    # http://python-gtk-3-tutorial.readthedocs.io/en/latest/objects.html#inherit-from-gobject-gobject
    __gsignals__ = {
    'status_update': (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self):
        Gtk.Window.__init__(self)
        
        self.queue = queue.Queue() # used for thread communication

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
        self.textView_2D.get_buffer().set_text(dfc.exampleText_2D) # initial text data
        self.textView_2D.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledTextWindow.add_with_viewport(self.textView_2D)   
        scrolledTextWindow.set_hexpand(True)
        scrolledTextWindow.set_vexpand(True)
        grid.attach(scrolledTextWindow, col, row, 1, 1) 

        row, col = (2, 2) # this will force the text entry height expansion
        l = Gtk.Label("\n\n\n\n\n\n\n\n")
        grid.attach(l, col, row, 1, 1)

        row, col = (2, 3)
        self.textView_3D = Gtk.TextView()
        self.textView_3D.get_buffer().set_text(dfc.exampleText_3D) # initial text data
        self.textView_3D.set_wrap_mode(Gtk.WrapMode.NONE)
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
        for exampleEquationText in dfc.eq_od2D.keys():
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
        for exampleEquationText in dfc.eq_od3D.keys():
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


    def do_status_update(self, unused):
        data = self.queue.get_nowait()
        
        if type(data) == type(''): # text is used for status box display to user
            self.statusWindow.UpdateStatusText(data)
        else: # the queue data is the fitted equation.
            # write the fitted equation to a pickle file.  This
            # allows the possibility of archiving the fitted equations
            pickledEquationFile = open("pickledEquationFile", "wb")
            pickle.dump(data, pickledEquationFile)
            pickledEquationFile.close()
    
            # view fitting results
            p = os.popen(sys.executable + ' FittingResultsViewer.py')
            p.close()
            
            # destroy the now-unused status box
            try: # was giving "id not found" errors on Linux
                self.statusWindow.destroy()
            except:
                pass


    def OnFit_2D(self, widget, data=None):
        textBuffer = self.textView_2D.get_buffer()
        startIter, endIter = textBuffer.get_bounds()
        textData = textBuffer.get_text(startIter, endIter, False)
        
        equationSelection = list(dfc.eq_od2D.keys())[self.equationSelect_2D]
        fittingTargetSelection = dfc.fittingTargetList[self.fittingTargetSelect_2D]
        
        # the GUI's fitting target string contains what we need - extract it
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od2D[equationSelection]
        eqString = 'pyeq3.Models_2D.' + item[0] + '(fittingTarget, ' + "'" + item[1] + "'" + item[2] + ')'
        self.equation = eval(eqString)

        # convert text to numeric data checking for log of negative numbers, etc.
        try:
            pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(textData, self.equation, False)
        except:
            messageBox = Gtk.MessageDialog(parent=None, 
                        flags=0,
                        type=Gtk.Message.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup(self.equation.reasonWhyDataRejected)
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()
            return

        # check for number of coefficients > number of data points to be fitted
        coeffCount = len(self.equation.GetCoefficientDesignators())
        dataCount = len(self.equation.dataCache.allDataCacheDictionary['DependentData'])
        if coeffCount > dataCount:
            messageBox = Gtk.MessageDialog(parent=None, 
                        flags=0,
                        type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup("This equation requires a minimum of " + str(coeffCount) + " data points, you have supplied " + repr(dataCount) + ".")
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()
            return
        
        self.statusWindow = StatusDialog.StatusWindow(self.queue)
        self.statusWindow.show()
        
        # thread will automatically start to run
        # "status update" handler will re-enable buttons
        self.fittingWorkerThread = FittingThread.FittingThread(self, self.equation)


    def OnFit_3D(self, widget, data=None):
        textBuffer = self.textView_3D.get_buffer()
        startIter, endIter = textBuffer.get_bounds()
        textData = textBuffer.get_text(startIter, endIter, False)
        
        equationSelection = list(dfc.eq_od3D.keys())[self.equationSelect_3D]
        fittingTargetSelection = dfc.fittingTargetList[self.fittingTargetSelect_3D]
        
        # the GUI's fitting target string contains what we need - extract it
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od3D[equationSelection]
        eqString = 'pyeq3.Models_3D.' + item[0] + '(fittingTarget, ' + "'" + item[1] + "'" + item[2] + ')'
        self.equation = eval(eqString)

        # convert text to numeric data checking for log of negative numbers, etc.
        try:
            pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(textData, self.equation, False)
        except:
            messageBox = Gtk.MessageDialog(parent=None, 
                        flags=0,
                        type=Gtk.Message.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup(self.equation.reasonWhyDataRejected)
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()
            return

        # check for number of coefficients > number of data points to be fitted
        coeffCount = len(self.equation.GetCoefficientDesignators())
        dataCount = len(self.equation.dataCache.allDataCacheDictionary['DependentData'])
        if coeffCount > dataCount:
            messageBox = Gtk.MessageDialog(parent=None, 
                        flags=0,
                        type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup("This equation requires a minimum of " + str(coeffCount) + " data points, you have supplied " + repr(dataCount) + ".")
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()
            return
        
        self.statusWindow = StatusDialog.StatusWindow(self.queue)
        self.statusWindow.show()
        
        # thread will automatically start to run
        # "status update" handler will re-enable buttons
        self.fittingWorkerThread = FittingThread.FittingThread(self, self.equation)


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
    win.set_position(Gtk.WindowPosition.CENTER)

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
