import pickle
import pyeq3
import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGtk version is less than 3.0, please upgrade'))

# local imports
import IndividualReports
import AdditionalInfo


class ResultsWindow(Gtk.Window):
    
    def __init__(self, pickledEquationFileName):
        Gtk.Window.__init__(self)

        self.graphReportsListForPDF = []
        self.textReportsListForPDF = []
        self.sourceCodeReportsListForPDF = []
        
        # first, load the fitted equation
        equationFile = open(pickledEquationFileName, 'rb')
        self.equation = pickle.load(equationFile)
        equationFile.close()

        # the "main" notebook at application top level
        nbTopLevel = Gtk.Notebook()
        
        nbGraphReports = Gtk.Notebook()
        nbTopLevel.append_page(nbGraphReports, Gtk.Label("Graph Reports"))

        nbTextReports = Gtk.Notebook()
        nbTopLevel.append_page(nbTextReports, Gtk.Label("Text Reports"))

        nbSourceCodeReports = Gtk.Notebook()
        nbTopLevel.append_page(nbSourceCodeReports, Gtk.Label("Source Code"))

        nbAdditionalInfo = Gtk.Notebook()
        nbTopLevel.append_page(nbAdditionalInfo, Gtk.Label("Additional Information"))
        
        self.add(nbTopLevel)
                
        # populate the "graph reports" top-level notebook tab
        if self.equation.GetDimensionality() == 2:
            report = IndividualReports.ModelScatterConfidenceGraph(self.equation, scatterplotOnlyFlag=False)
            reportTitle = "Model With 95%Confidence"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
            report = IndividualReports.ModelScatterConfidenceGraph(self.equation, scatterplotOnlyFlag=True)
            reportTitle = "Scatter Plot"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])
        else:
            report = IndividualReports.SurfacePlot(self.equation)
            reportTitle = "Surface Plot"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
            report = IndividualReports.ContourPlot(self.equation)
            reportTitle = "Contour Plot"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
            report = IndividualReports.ScatterPlot(self.equation)
            reportTitle = "Scatter Plot"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])
            
        report = IndividualReports.AbsoluteErrorGraph(self.equation)
        reportTitle = "Absolute Error"
        nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
        self.graphReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.AbsoluteErrorHistogram(self.equation)
        reportTitle = "Absolute Error Histogram"
        nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
        self.graphReportsListForPDF.append([report[1], reportTitle])

        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.PercentErrorGraph(self.equation)
            reportTitle = "Percent Error"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])

            report = IndividualReports.PercentErrorHistogram(self.equation)
            reportTitle = "Percent Error Histogram"
            nbGraphReports.append_page(report[0], Gtk.Label(reportTitle))
            self.graphReportsListForPDF.append([report[1], reportTitle])

        # populate the "text reports" top-level notebook tab
        report = IndividualReports.CoefficientAndFitStatistics(self.equation)
        reportTitle = "Coefficient And Fit Statistics"
        nbTextReports.append_page(report[0], Gtk.Label(reportTitle))
        self.textReportsListForPDF.append([report[1], reportTitle])
        
        report = IndividualReports.CoefficientListing(self.equation)
        reportTitle = "Coefficient Listing"
        nbTextReports.append_page(report[0], Gtk.Label(reportTitle))
        self.textReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.DataArrayStatisticsReport('Absolute Error Statistics', self.equation.modelAbsoluteError)
        reportTitle = "Absolute Error Statistics"
        nbTextReports.append_page(report[0], Gtk.Label(reportTitle))
        self.textReportsListForPDF.append([report[1], reportTitle])

        
        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.DataArrayStatisticsReport('Percent Error Statistics', self.equation.modelPercentError)
            reportTitle = "Percent Error Statistics"
            nbTextReports.append_page(report[0], Gtk.Label(reportTitle))
            self.textReportsListForPDF.append([report[1], reportTitle])

        # populate the "source code" top-level notebook tab
        report = IndividualReports.SourceCodeReport(self.equation, 'CPP')
        reportTitle = "C++"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'CSHARP')
        reportTitle = "CSHARP"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'VBA')
        reportTitle = "VBA"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'PYTHON')
        reportTitle = "PYTHON"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'JAVA')
        reportTitle = "JAVA"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'JAVASCRIPT')
        reportTitle = "JAVASCRIPT"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'JULIA')
        reportTitle = "JULIA"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'SCILAB')
        reportTitle = "SCILAB"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'MATLAB')
        reportTitle = "MATLAB"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        report = IndividualReports.SourceCodeReport(self.equation, 'FORTRAN90')
        reportTitle = "FORTRAN90"
        nbSourceCodeReports.append_page(report[0], Gtk.Label(reportTitle))
        self.sourceCodeReportsListForPDF.append([report[1], reportTitle])

        # populate the "additional information" top-level notebook tab
        historyTextView = Gtk.TextView()
        historyTextView.get_buffer().set_text(AdditionalInfo.history)
        historyTextView.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolledHistoryText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledHistoryText.add_with_viewport(historyTextView)
        nbAdditionalInfo.append_page(scrolledHistoryText, Gtk.Label("Fitting History"))
        
        authorTextView = Gtk.TextView()
        authorTextView.get_buffer().set_text(AdditionalInfo.author)
        authorTextView.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolledAuthorText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledAuthorText.add_with_viewport(authorTextView)
        nbAdditionalInfo.append_page(scrolledAuthorText, Gtk.Label("Author History"))
        
        linksTextView = Gtk.TextView()
        linksTextView.get_buffer().set_text(AdditionalInfo.links)
        linksTextView.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolledLinksText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledLinksText.add_with_viewport(linksTextView)
        nbAdditionalInfo.append_page(scrolledLinksText, Gtk.Label("Web Links"))

        # populate the "list of all equations" top-level notebook tab
        dim = self.equation.GetDimensionality()
        allEquationaTextView = Gtk.TextView()

        # pass the textView's textbuffer for processing of bold, italic, etc.
        newBuffer = IndividualReports.AllEquationReport(dim, allEquationaTextView.get_buffer())
        allEquationaTextView.set_buffer(newBuffer)
            
        allEquationaTextView.set_wrap_mode(Gtk.WrapMode.NONE)
        scrolledAllEquationsText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledAllEquationsText.add_with_viewport(allEquationaTextView)

        nbTopLevel.append_page(scrolledAllEquationsText, Gtk.Label("List Of All Standard " + str(dim) + "D Equations"))

        # the "Save To PDF" tab
        btn = Gtk.Button(label = "Save To PDF")
        btn.connect("clicked", self.createPDF, None)
        
        vbox = Gtk.VButtonBox()
        vbox.pack_start(btn, False, False, 0)
         
        nbTopLevel.append_page(vbox, Gtk.Label("Save To PDF File"))


    def createPDF(self, widget, data=None):
        try:
            import reportlab
        except:
            messageBox = Gtk.MessageDialog(parent=self, 
                        flags=0,
                        type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup("\nCould not import reportlab.\n\nPlease install using the command\n\n'pip3 install reportlab'")
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()
            return
            
        # see http://python-gtk-3-tutorial.readthedocs.io/en/latest/dialogs.html?highlight=FileChooserDialog
        pdfChoooser = Gtk.FileChooserDialog(
                                "PDF file name",
                                self,
                                Gtk.FileChooserAction.SAVE,
                                (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK)
                                )
        filter1 = Gtk.FileFilter()
        filter1.set_name("PDF Files (*.pdf)")
        filter1.add_pattern("*.pdf")
        pdfChoooser.add_filter(filter1)
        
        filter2 = Gtk.FileFilter()
        filter2.set_name("All Riles")
        filter2.add_pattern("*")
        pdfChoooser.add_filter(filter2)
        
        fName = ''
        response = pdfChoooser.run()
        if response == Gtk.ResponseType.OK:
            fName = pdfChoooser.get_filename()
        pdfChoooser.destroy()

        if fName:
            import pdfCode
            pdfCode.CreatePDF(fName,
                              self.equation,
                              self.graphReportsListForPDF,
                              self.textReportsListForPDF,
                              self.sourceCodeReportsListForPDF
                              )
            messageBox = Gtk.MessageDialog(parent=None, 
                        flags=0,
                        type=Gtk.MessageType.INFO,
                        buttons=Gtk.ButtonsType.OK,
                        message_format=None)
            messageBox.set_markup("\nSuccessfully created PDF file.")
            messageBox.set_transient_for(self)
            messageBox.run()
            messageBox.destroy()



if __name__ == "__main__":
    win = ResultsWindow(pickledEquationFileName='pickledEquationFile')
    win.set_title("Example pyGtk - Fitting Results Viewer")

    win.set_size_request(800, 600) # minimum screen size
    win.set_position(Gtk.WindowPosition.CENTER)

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
