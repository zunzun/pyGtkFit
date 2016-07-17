import pickle, inspect, re
import pyeq3
import numpy, scipy

import warnings, gi

# gi.require_version('Gtk', '3.0')
with warnings.catch_warnings(record=True):
    from gi.repository import Gtk
if Gtk.get_major_version() < 3:
    raise(Exception('Detected pyGTK version is less than 3.0, please upgrade'))

from gi.repository import Pango # for pygtk text bold, italic, etc.

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

from mpl_toolkits.mplot3d import  Axes3D
from matplotlib import cm # to colormap 3D surfaces from blue to red
import matplotlib.pyplot


# 3D contour plot lines
numberOfContourLines = 16

# this is used in several reports
def DataArrayStatisticsReport(titleString, tempdata):
    rawText = ''
    rawText += titleString + '\n\n'
    
    # must at least have max and min
    minData = min(tempdata)
    maxData = max(tempdata)
    
    if maxData == minData:
        rawText += 'All data has the same value,\n'
        rawText += "value = %-.16E\n" % (minData)
        rawText += 'statistics cannot be calculated.'
    else:
        rawText += "max = %-.16E\n" % (maxData)
        rawText += "min = %-.16E\n" % (minData)
        
        try:
            temp = scipy.mean(tempdata)
            rawText += "mean = %-.16E\n" % (temp)
        except:
            rawText += "mean gave error in calculation\n"

        try:
            temp = scipy.stats.sem(tempdata)
            rawText += "standard error of mean = %-.16E\n" % (temp)
        except:
            rawText += "standard error of mean gave error in calculation\n"

        try:
            temp = scipy.median(tempdata)
            rawText += "median = %-.16E\n" % (temp)
        except:
            rawText += "median gave error in calculation\n"

        try:
            temp = scipy.var(tempdata)
            rawText += "variance = %-.16E\n" % (temp)
        except:
            rawText += "variance gave error in calculation\n"

        try:
            temp = scipy.std(tempdata)
            rawText += "std. deviation = %-.16E\n" % (temp)
        except:
            rawText += "std. deviation gave error in calculation\n"

        try:
            temp = scipy.stats.skew(tempdata)
            rawText += "skew = %-.16E\n" % (temp)
        except:
            rawText += "skew gave error in calculation\n"

        try:
            temp = scipy.stats.kurtosis(tempdata)
            rawText += "kurtosis = %-.16E\n" % (temp)
        except:
            rawText += "kurtosis gave error in calculation\n"
            
    textView = Gtk.TextView()
    textView.get_buffer().set_text(rawText)
    textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
    scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
    scrolledTextWindow.add_with_viewport(textView)    
    return scrolledTextWindow
    

def CoefficientAndFitStatistics(equation):
    rawText = ''
    if equation.upperCoefficientBounds or equation.lowerCoefficientBounds:
        rawText += 'This model has coefficient bounds. Parameter statistics may\n'
        rawText += 'not be valid for parameter values at or near the bounds.\n'
        rawText += '\n'
    
    rawText += 'Degress of freedom error ' + str(equation.df_e) + '\n'
    rawText += 'Degress of freedom regression ' + str(equation.df_r) + '\n'
    
    if equation.rmse == None:
        rawText += 'Root Mean Squared Error (RMSE): n/a\n'
    else:
        rawText += 'Root Mean Squared Error (RMSE): ' + str(equation.rmse) + '\n'
    
    if equation.r2 == None:
        rawText += 'R-squared: n/a\n'
    else:
        rawText += 'R-squared: ' + str(equation.r2) + '\n'
    
    if equation.r2adj == None:
        rawText += 'R-squared adjusted: n/a\n'
    else:
        rawText += 'R-squared adjusted: ' + str(equation.r2adj) + '\n'
    
    if equation.Fstat == None:
        rawText += 'Model F-statistic: n/a\n'
    else:
        rawText += 'Model F-statistic: ' + str(equation.Fstat) + '\n'
    
    if equation.Fpv == None:
        rawText += 'Model F-statistic p-value: n/a\n'
    else:
        rawText += 'Model F-statistic p-value: ' + str(equation.Fpv) + '\n'
    
    if equation.ll == None:
        rawText += 'Model log-likelihood: n/a\n'
    else:
        rawText += 'Model log-likelihood: ' + str(equation.ll) + '\n'
    
    if equation.aic == None:
        rawText += 'Model AIC: n/a\n'
    else:
        rawText += 'Model AIC: ' + str(equation.aic) + '\n'
    
    if equation.bic == None:
        rawText += 'Model BIC: n/a\n'
    else:
        rawText += 'Model BIC: ' + str(equation.bic) + '\n'
        
    rawText += '\n'
    rawText += "Individual Parameter Statistics:\n"
    for i in range(len(equation.solvedCoefficients)):
        if type(equation.tstat_beta) == type(None):
            tstat = 'n/a'
        else:
            tstat = '%-.5E' %  (equation.tstat_beta[i])
    
        if type(equation.pstat_beta) == type(None):
            pstat = 'n/a'
        else:
            pstat = '%-.5E' %  ( equation.pstat_beta[i])
    
        if type(equation.sd_beta) != type(None):
            rawText += "Coefficient %s = %-.16E, std error: %-.5E\n" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i], equation.sd_beta[i])
        else:
            rawText += "Coefficient %s = %-.16E, std error: n/a\n" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i])
        rawText += "          t-stat: %s, p-stat: %s, 95 percent confidence intervals: [%-.5E, %-.5E]\n" % (tstat,  pstat, equation.ci[i][0], equation.ci[i][1])
            
    rawText += '\n'
    rawText += "Coefficient Covariance Matrix:\n"
    for i in  equation.cov_beta:
        rawText += str(i) + '\n'
        
    textView = Gtk.TextView()
    textView.get_buffer().set_text(rawText)
    textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
    scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
    scrolledTextWindow.add_with_viewport(textView)    
    return scrolledTextWindow


def CoefficientListing(equation):
    rawText = ''
    cd = equation.GetCoefficientDesignators()
    for i in range(len(equation.solvedCoefficients)):
        rawText += "%s = %-.16E\n" % (cd[i], equation.solvedCoefficients[i])

    textView = Gtk.TextView()
    textView.get_buffer().set_text(rawText)
    textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
    scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
    scrolledTextWindow.add_with_viewport(textView)    
    return scrolledTextWindow


def SourceCodeReport(equation, lanuageNameString):
    textView = Gtk.TextView()
    rawText = eval('pyeq3.outputSourceCodeService().GetOutputSourceCode' + lanuageNameString + '(equation)')
    textView.get_buffer().set_text(rawText)
    textView.set_wrap_mode(0) # 0 = no wrap, using Gtk.WRAP_NONE failed in developemnt
    scrolledTextWindow = Gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
    scrolledTextWindow.add_with_viewport(textView)    
    return scrolledTextWindow


def AbsoluteErrorGraph(equation):
    f = Figure()
    axes = f.add_subplot(111)
    dep_data = equation.dataCache.allDataCacheDictionary['DependentData']
    abs_error = equation.modelAbsoluteError
    axes.plot(dep_data, abs_error, 'D')
    
    if equation.GetDimensionality() == 2: # used for labels only
        axes.set_title('Absolute Error vs. X Data')
        axes.set_xlabel('X Data')
    else:
        axes.set_title('Absolute Error vs. Z Data')
        axes.set_xlabel('Z Data')
        
    axes.set_ylabel(" Absolute Error") # Y axis label is always absolute error
    
    return FigureCanvas(f) # a Gtk.DrawingArea 


def PercentErrorGraph(equation):
    f = Figure()
    axes = f.add_subplot(111)
    dep_data = equation.dataCache.allDataCacheDictionary['DependentData']
    per_error = equation.modelPercentError
    axes.plot(dep_data, per_error, 'D')
    
    if equation.GetDimensionality() == 2: # used for labels only
        axes.set_title('Percent Error vs. X Data')
        axes.set_xlabel('X Data')
    else:
        axes.set_title('Percent Error vs. Z Data')
        axes.set_xlabel('Z Data')
        
    axes.set_ylabel(" Percent Error") # Y axis label is always Percent error
    
    return FigureCanvas(f) # a Gtk.DrawingArea 


def AbsoluteErrorHistogram(equation):
    f = Figure()
    axes = f.add_subplot(111)
    abs_error = equation.modelAbsoluteError
    bincount = len(abs_error)//2 # integer division
    if bincount < 5:
        bincount = 5
    if bincount > 25:
        bincount = 25
    n, bins, patches = axes.hist(abs_error, bincount, rwidth=0.8)
    
    # some axis space at the top of the graph
    ylim = axes.get_ylim()
    if ylim[1] == max(n):
        axes.set_ylim(0.0, ylim[1] + 1)

    axes.set_title('Absolute Error Histogram') # add a title
    axes.set_xlabel('Absolute Error') # X axis data label
    axes.set_ylabel(" Frequency") # Y axis label is frequency

    return FigureCanvas(f) # a Gtk.DrawingArea 


def PercentErrorHistogram(equation):
    f = Figure()
    axes = f.add_subplot(111)
    abs_error = equation.modelPercentError
    bincount = len(abs_error)//2 # integer division
    if bincount < 5:
        bincount = 5
    if bincount > 25:
        bincount = 25
    n, bins, patches = axes.hist(abs_error, bincount, rwidth=0.8)
    
    # some axis space at the top of the graph
    ylim = axes.get_ylim()
    if ylim[1] == max(n):
        axes.set_ylim(0.0, ylim[1] + 1)

    axes.set_title('Percent Error Histogram') # add a title
    axes.set_xlabel('Percent Error') # X axis data label
    axes.set_ylabel(" Frequency") # Y axis label is frequency

    return FigureCanvas(f) # a Gtk.DrawingArea 


def ModelScatterConfidenceGraph(equation):
    f = Figure()
    axes = f.add_subplot(111)
    y_data = equation.dataCache.allDataCacheDictionary['DependentData']
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]

    # create data for the fitted equation plot
    xModel = numpy.linspace(min(x_data), max(x_data))

    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([xModel, xModel])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    yModel = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache # restore the original data cache

    # first the raw data as a scatter plot
    axes.plot(x_data, y_data,  'D')

    # now the model as a line plot
    axes.plot(xModel, yModel)

    # now calculate confidence intervals
    # http://support.sas.com/documentation/cdl/en/statug/63347/HTML/default/viewer.htm#statug_nlin_sect026.htm
    # http://www.staff.ncl.ac.uk/tom.holderness/software/pythonlinearfit
    mean_x = numpy.mean(x_data)
    n = equation.nobs

    t_value = scipy.stats.t.ppf(0.975, equation.df_e) # (1.0 - (a/2)) is used for two-sided t-test critical value, here a = 0.05

    confs = t_value * numpy.sqrt((equation.sumOfSquaredErrors/equation.df_e)*(1.0/n + (numpy.power((xModel-mean_x),2.0)/
                                                                                       ((numpy.sum(numpy.power(x_data,2.0)))-n*(numpy.power(mean_x,2.0))))))

    # get lower and upper confidence limits based on predicted y and confidence intervals
    upper = yModel + abs(confs)
    lower = yModel - abs(confs)

    # mask off any numbers outside the existing plot limits
    booleanMask = yModel > axes.get_ylim()[0]
    booleanMask &= (yModel < axes.get_ylim()[1])

    # color scheme improves visibility on black background lines or points
    axes.plot(xModel[booleanMask], lower[booleanMask], linestyle='solid', color='white')
    axes.plot(xModel[booleanMask], upper[booleanMask], linestyle='solid', color='white')
    axes.plot(xModel[booleanMask], lower[booleanMask], linestyle='dashed', color='blue')
    axes.plot(xModel[booleanMask], upper[booleanMask], linestyle='dashed', color='blue')

    axes.set_title('Model With 95% Confidence Intervals') # add a title
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label

    return FigureCanvas(f) # a Gtk.DrawingArea 


def SurfacePlot(equation):
    f = matplotlib.pyplot.figure() # using pyplot
    FigureCanvas(f)

    axes = f.add_subplot(111, projection='3d')
    
    matplotlib.pyplot.grid(True)
    
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    xModel = numpy.linspace(min(x_data), max(x_data), 20)
    yModel = numpy.linspace(min(y_data), max(y_data), 20)
    X, Y = numpy.meshgrid(xModel, yModel)

    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([X, Y])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    Z = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache# restore the original data cache

    axes.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)

    axes.scatter(x_data, y_data, z_data)

    axes.set_title('Surface Plot') # add a title for surface plot
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label
    axes.set_zlabel('Z Data') # Z axis data label

    matplotlib.pyplot.close('all') # clean up after using pyplot or else there can be memory and process problems
    return FigureCanvas(f) # a Gtk.DrawingArea 


def ContourPlot(equation):
    f = matplotlib.pyplot.figure() # using pyplot
    FigureCanvas(f)
    
    axes = f.add_subplot(111)

    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    xModel = numpy.linspace(min(x_data), max(x_data), 20)
    yModel = numpy.linspace(min(y_data), max(y_data), 20)
    X, Y = numpy.meshgrid(xModel, yModel)
        
    tempcache = equation.dataCache # store the data cache
    equation.dataCache = pyeq3.dataCache()
    equation.dataCache.allDataCacheDictionary['IndependentData'] = numpy.array([X, Y])
    equation.dataCache.FindOrCreateAllDataCache(equation)
    Z = equation.CalculateModelPredictions(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.dataCache = tempcache # restore the original data cache
        
    axes.plot(x_data, y_data, 'o')

    axes.set_title('Contour Plot') # add a title for contour plot
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label
        
    CS = matplotlib.pyplot.contour(X, Y, Z, numberOfContourLines, colors='k')
    matplotlib.pyplot.clabel(CS, inline=1, fontsize=10) # labels for contours

    matplotlib.pyplot.close('all') # clean up after using pyplot or else there can be memory and process problems
    return FigureCanvas(f) # a Gtk.DrawingArea


def ScatterPlot(equation):
    f = matplotlib.pyplot.figure() # using pyplot
    FigureCanvas(f)

    axes = f.add_subplot(111, projection='3d')
    
    matplotlib.pyplot.grid(True)
    
    x_data = equation.dataCache.allDataCacheDictionary['IndependentData'][0]
    y_data = equation.dataCache.allDataCacheDictionary['IndependentData'][1]
    z_data = equation.dataCache.allDataCacheDictionary['DependentData']
            
    axes.scatter(x_data, y_data, z_data)

    axes.set_title('Scatter Plot')
    axes.set_xlabel('X Data')
    axes.set_ylabel('Y Data')
    axes.set_zlabel('Z Data')
    
    matplotlib.pyplot.close('all') # clean up after using pyplot or else there can be memory and process problems
    return FigureCanvas(f) # a Gtk.DrawingArea


def AllEquationReport(dim, textBuffer):

    tag_bold = textBuffer.create_tag(weight = Pango.Weight.BOLD)
    tag_italic = textBuffer.create_tag(style = Pango.Style.ITALIC)
    tag_superscript = textBuffer.create_tag(rise=6 * Pango.SCALE)
    tag_subscript = textBuffer.create_tag(rise=-6 * Pango.SCALE)
    
    if dim == 2:
        module = pyeq3.Models_2D
    else:
        module = pyeq3.Models_3D
     
    for submodule in inspect.getmembers(module):
        if inspect.ismodule(submodule[1]):
            for equationClass in inspect.getmembers(submodule[1]):
                if inspect.isclass(equationClass[1]):
                    for extendedVersionName in ['Default', 'Offset']:
                        
                        # if the equation *already* has an offset,
                        # do not add an offset version here
                        if (-1 != extendedVersionName.find('Offset')) and (equationClass[1].autoGenerateOffsetForm == False):
                            continue

                        equation = equationClass[1]('SSQABS', extendedVersionName)

                        equationName = equation.GetDisplayName()
                        moduleName = str(dim) + 'D ' + submodule[0]
                        
                        startIter = textBuffer.get_end_iter()
                        textBuffer.insert_with_tags(startIter, moduleName, tag_bold)

                        startIter = textBuffer.get_end_iter()
                        textBuffer.insert(startIter,  '  ')

                        startIter = textBuffer.get_end_iter()
                        textBuffer.insert_with_tags(startIter, equationName, tag_italic)

                        startIter = textBuffer.get_end_iter()
                        textBuffer.insert(startIter,  '   ')

                        # html <br> tags become new line characters
                        html = equation.GetDisplayHTML().replace('<br>', '\n')
                        
                        # display pyeq3's html superscript and subscript tags
                        #  pyeq3's html has no nested HTML tags, so no recursion
                        findIter = re.finditer(r'<su.>|</su.>', html)
                        currentIndex = 0
                        endingIndex = len(html)
                        itemCount = 0
                        for item in findIter:
                            span = item.span()
                            if not itemCount % 2: # text is *not* within HTML tags
                                t = html[currentIndex:span[0]]
                                startIter = textBuffer.get_end_iter()
                                textBuffer.insert(startIter,  t)
                                currentIndex = span[1] # beginning tag
                            else: # text *is* within html tags
                                if html[span[1]-2] == 'b': # subscript tag
                                    tag = tag_subscript
                                else: # html superscript tag
                                    tag = tag_superscript
                                t = html[currentIndex:span[1]-6]
                                startIter = textBuffer.get_end_iter()
                                textBuffer.insert_with_tags(startIter, t, tag)
                                currentIndex = span[1] # ending tag
                            itemCount += 1

                        # any ending text, or if no tags were found
                        if currentIndex < endingIndex:
                            t = html[currentIndex:endingIndex]
                            startIter = textBuffer.get_end_iter()
                            textBuffer.insert(startIter, t)
                            
                        startIter = textBuffer.get_end_iter()
                        textBuffer.insert(startIter, '\n')
                                                
    return textBuffer
