import pickle
import pyeq3
import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))

# local imports
import IndividualReports
import AdditionalInfo


class ResultsWindow(Gtk.Window):
    
    def __init__(self, pickledEquationFileName):
        Gtk.Window.__init__(self)
        
        # first, load the fitted equation
        equationFile = open(pickledEquationFileName, 'rb')
        equation = pickle.load(equationFile)
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
        if equation.GetDimensionality() == 2:
            report = IndividualReports.ModelScatterConfidenceGraph(equation)
            nbGraphReports.append_page(report, Gtk.Label("Model With 95%Confidence"))
        else:
            report = IndividualReports.SurfacePlot(equation)
            nbGraphReports.append_page(report, Gtk.Label("Surface Plot"))
            
            report = IndividualReports.ContourPlot(equation)
            nbGraphReports.append_page(report, Gtk.Label("Contour Plot"))
            
            report = IndividualReports.ScatterPlot(equation)
            nbGraphReports.append_page(report, Gtk.Label("Scatter Plot"))
            
        report = IndividualReports.AbsoluteErrorGraph(equation)
        nbGraphReports.append_page(report, Gtk.Label("Absolute Error"))

        report = IndividualReports.AbsoluteErrorHistogram(equation)
        nbGraphReports.append_page(report, Gtk.Label("Absolute Error Histogram"))

        if equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.PercentErrorGraph(equation)
            nbGraphReports.append_page(report, Gtk.Label("Percent Error"))

            report = IndividualReports.PercentErrorHistogram(equation)
            nbGraphReports.append_page(report, Gtk.Label("Percent Error Histogram"))

        # populate the "text reports" top-level notebook tab
        report = IndividualReports.CoefficientAndFitStatistics(equation)
        nbTextReports.append_page(report, Gtk.Label("Coefficient And Fit Statistics"))
        
        report = IndividualReports.CoefficientListing(equation)
        nbTextReports.append_page(report, Gtk.Label("Coefficient Listing"))

        report = IndividualReports.DataArrayStatisticsReport('Absolute Error Statistics', equation.modelAbsoluteError)
        nbTextReports.append_page(report, Gtk.Label("Absolute Error Statistics"))
        
        if equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = IndividualReports.DataArrayStatisticsReport('Percent Error Statistics', equation.modelPercentError)
            nbTextReports.append_page(report, Gtk.Label("Percent Error Statistics"))

        # populate the "source code" top-level notebook tab
        report = IndividualReports.SourceCodeReport(equation, 'CPP')
        nbSourceCodeReports.append_page(report, Gtk.Label("C++"))

        report = IndividualReports.SourceCodeReport(equation, 'CSHARP')
        nbSourceCodeReports.append_page(report, Gtk.Label("CSHARP"))

        report = IndividualReports.SourceCodeReport(equation, 'VBA')
        nbSourceCodeReports.append_page(report, Gtk.Label("VBA"))

        report = IndividualReports.SourceCodeReport(equation, 'PYTHON')
        nbSourceCodeReports.append_page(report, Gtk.Label("PYTHON"))

        report = IndividualReports.SourceCodeReport(equation, 'JAVA')
        nbSourceCodeReports.append_page(report, Gtk.Label("JAVA"))

        report = IndividualReports.SourceCodeReport(equation, 'JAVASCRIPT')
        nbSourceCodeReports.append_page(report, Gtk.Label("JAVASCRIPT"))

        report = IndividualReports.SourceCodeReport(equation, 'JULIA')
        nbSourceCodeReports.append_page(report, Gtk.Label("JULIA"))

        report = IndividualReports.SourceCodeReport(equation, 'SCILAB')
        nbSourceCodeReports.append_page(report, Gtk.Label("SCILAB"))

        report = IndividualReports.SourceCodeReport(equation, 'MATLAB')
        nbSourceCodeReports.append_page(report, Gtk.Label("MATLAB"))

        report = IndividualReports.SourceCodeReport(equation, 'FORTRAN90')
        nbSourceCodeReports.append_page(report, Gtk.Label("FORTRAN90"))

        # populate the "additional information" top-level notebook tab
        historyTextView = Gtk.TextView()
        historyTextView.get_buffer().set_text(AdditionalInfo.history)
        historyTextView.set_wrap_mode(2) # 2 = word wrap, using Gtk.WRAP_WORD failed in developemnt
        scrolledHistoryText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledHistoryText.add_with_viewport(historyTextView)
        nbAdditionalInfo.append_page(scrolledHistoryText, Gtk.Label("Fitting History"))
        
        authorTextView = Gtk.TextView()
        authorTextView.get_buffer().set_text(AdditionalInfo.author)
        authorTextView.set_wrap_mode(2) # 2 = word wrap, using Gtk.WRAP_WORD failed in developemnt
        scrolledAuthorText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledAuthorText.add_with_viewport(authorTextView)
        nbAdditionalInfo.append_page(scrolledAuthorText, Gtk.Label("Author History"))
        
        linksTextView = Gtk.TextView()
        linksTextView.get_buffer().set_text(AdditionalInfo.links)
        linksTextView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledLinksText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledLinksText.add_with_viewport(linksTextView)
        nbAdditionalInfo.append_page(scrolledLinksText, Gtk.Label("Web Links"))

        # populate the "list of all equations" top-level notebook tab
        dim = equation.GetDimensionality()
        allEquationaTextView = Gtk.TextView()

        # pass the textView's textbuffer for bold, italic, etc.
        newBuffer = IndividualReports.AllEquationReport(dim, allEquationaTextView.get_buffer())
        allEquationaTextView.set_buffer(newBuffer)
            
        allEquationaTextView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
        scrolledAllEquationsText = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        scrolledAllEquationsText.add_with_viewport(allEquationaTextView)

        nbTopLevel.append_page(scrolledAllEquationsText, Gtk.Label("List Of All Standard " + str(dim) + "D Equations"))



if __name__ == "__main__":
    win = ResultsWindow(pickledEquationFileName='pickledEquationFile')
    win.set_title("Example pyGtk - Fitting Results Viewer")

    win.set_size_request(800, 600) # minimum screen size

    # pyGtk allows multiple windows for a single process.  We must
    # connect this window's exit code to the Gtk main process exit code,
    # or pyGtk itself will not know to exit when the window is closed.
    win.connect("delete-event", Gtk.main_quit)

    win.show_all()
    Gtk.main()
