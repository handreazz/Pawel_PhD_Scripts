"""
A histogram class that inherits from the numpy.ndarray object
"""

import copy, itertools, math
import numpy, scipy
import matplotlib

from matplotlib import axes, figure, pyplot, cm

class Histogram(numpy.ndarray):
    def __new__(subtype, input_array, edges=None):
        '''
        Input array is an already formed ndarray instance
        We first cast to be our class type

        add the new attributes to the created instance

        Finally, we must return the newly created object
        '''
        obj = numpy.asarray(input_array).view(subtype)
        obj.edges = edges
        return obj

    def __array_finalize__(self, obj):
        '''
        ``self`` is a new object resulting from ndarray.__new__(Histogram, ...), therefore it only has attributes that the ndarray.__new__ constructor gave it - i.e. those of a standard ndarray.

        We could have got to the ndarray.__new__ call in 3 ways:
        From an explicit constructor - e.g. Histogram():
            obj is None
            (we're in the middle of the Histogram.__new__ constructor, and self.extent will be set when we return to Histogram.__new__)
        From view casting - e.g arr.view(Histogram):
            obj is arr
            (type(obj) can be Histogram)
        From new-from-template - e.g hist[:3]
            type(obj) is Histogram

        Note that it is here, rather than in the __new__ method, that we set the default value for 'extent', because this method sees all creation of default objects - with the Histogram.__new__ constructor, but also with arr.view(Histogram).

        edges is one of these two:
            a list of len(self.shape) arrays describing the bin edges for each dimension. The number of edges in dimension i (counting from 0) for example is len(self.shape[i] + 1)
        or:
            a sequence of paired floats indicating the min and max of each dimension, in the latter case, the number of bins in each in each dimension is taken from self.shape and are uniformly divided along this dimension.

        1-dimension:
        10 evenly spaced bins can be described in these ways:
        edges = arange(0., 1.0001, 0.01)
        edges = numpy.linspace(0, 1, 11)
        edges = [0., 1.]

        2-dimensions:
        edges = [[xmin, xmax], [ymin, ymax]]

        '''
        if obj is None: return
        self.edges = getattr(obj, 'edges', None)

    def __array_wrap__(self, out_arr, context=None):
        '''
        __array_wrap__ gets called at the end of numpy ufuncs and other numpy functions, to allow a subclass to set the type of the return value and update attributes and metadata.

        fist, call the parent's __array_wrap__
        then transfer the self.__dict__ attributes to the new
        histogram (obj) and return it. Do nothing if the
        input histogram has no attributes (KeyError).
        '''
        obj = numpy.ndarray.__array_wrap__(self, out_arr, context)

        try:
            for name in vars(self):
                setattr(obj, name, vars(self)[name])
        except KeyError: pass

        return obj

    def extent(self):
        '''
        returns the extent of the data
        to be used by the plotting method.

        [xmin, xmax, ymin, ymax ...]
        '''
        ext = []
        for e in self.edges:
            ext += [e[0], e[-1]]
        return ext

    def dim(self):
        '''
        returns the dimension of the histogram
        '''
        return len(self.shape)

    def aspolygon(self, ymin=0, range=None):
        '''
        returns a polygon of the histogram which is a series of points
        starting and ending at the lower-left-most point

        also returns the extent [xmin, xmax, ymin, ymax] of the polygon
        '''
        if not self.dim() is 1:
            raise Exception('only 1D histograms can be translated into a polygon.')

        if len(self.edges[0]) == 2:
            edges = numpy.linspace(edges[0][0], edges[0][-1], self.shape[0])
        else:
            edges = self.edges[0]

        '''
        s = [s0, s1, s2, s3 ...]
        chain.from_iterable(izip(*tee(s)))
            = [s0, s0, s1, s1, s2, s2, s3, s3 ...]
        '''
        # setup x and y position iterators for entire histogram
        xarr = itertools.chain.from_iterable(itertools.izip(*itertools.tee(edges)))
        yarr = itertools.chain.from_iterable(itertools.izip(*itertools.tee(self)))

        # increment the x position
        next(xarr,None)

        if range is None:
            '''
            returns the entire histogram as a polygon starting
            and ending with the "first" point
            '''
            first = [(edges[0], ymin)]
            points = [x for x in itertools.chain(
                first,
                itertools.izip(xarr, yarr),
                [(edges[-1], ymin)],
                first)]

            extent = [edges[0], edges[-1], min(min(self), ymin), max(self)]

        else:
            '''
            returns the histogram within a certain range in x
            as a polygon

            if the limits specified are outside the edge range
            of the histogram then they are overridden by
            self.edge[0][0] and self.edge[0][-1]

            it is implied that self.edge[0] must
            be a monotomically increasing list.
            '''
            xmin = max(range[0], edges[0])
            xmax = min(range[-1], edges[-1])

            first = (xmin, ymin)

            isfirst = True
            prev = (xmin, self[0])

            points = [first]
            for p in itertools.izip(xarr, yarr):
                if p[0] > xmin:
                    if isfirst:
                        points += [prev]
                        isfirst = False
                    if p[0] < xmax:
                        points += [p]
                if isfirst:
                    prev = (xmin, p[1])
                if p[0] > xmax:
                    break
            points += [(xmax, points[-1][1]), (xmax, ymin), first]

            extent = [xmin, xmax, min(min(zip(*points)[1]), ymin), max(zip(*points)[1])]

        return (points, extent)

    def grid(self):
        '''
        returns an array (1 or 2 dimensional) of the
        center-point of each bin.

        Useful for converting a histogram to a line or
        surface plot:

        1D histogram:
            x, y = hist.grid(), hist
            plot(x, y)

        2D histogram:
            x, y = hist.grid()
            z = hist
            surface_plot(x, y, z)
        '''
        if not self.dim() in [1, 2]:
            raise Exception('only 1D and 2D histograms can return a grid.')
        if self.dim() is 1:
            it1, it2 = itertools.tee(iter(self.edges[0]))
            next(it2)
            return numpy.array([0.5 * (i1 + i2) for i1, i2 in itertools.izip(it1, it2)])
        if self.dim() is 2:
            grid = [[],[]]
            for d in [0, 1]:
                it1, it2 = itertools.tee(iter(self.edges[d]))
                next(it2)
                for i1, i2 in itertools.izip(it1, it2):
                    grid[d] += [0.5 * (i1 + i2)]
            return numpy.meshgrid(grid[0], grid[1])

    def cut(self, range):
        '''
        returns a new histogram over a sub-range of the current one.
        expands the range to the outer bounds the bins that contain
        the specified limits.

        note: not implemented for dimension > 1 yet!
        '''
        if not self.dim() in [1]:
            raise Exception('only 1D histograms can be cut.')
        hnew = []
        enew = []
        for x, h, e in zip(self.grid(), self, self.edges[0]):
            if (range[0] < x) and (x < range[1]):
                hnew.append(h)
                enew.append(e)
            elif len(enew) in [0,1]:
                enew = [e]
            else:
                hnew.append(h)
                enew.append(e)
                break
        return Histogram(hnew, [enew])

    def rebin(self, bins, range):
        '''
        rebins the histogram in an arbitrary way. The bins and range
        options are eventually passed to numpy.histogramdd().

        The sample data is taken as the mid point of each bin, weighted
        by the histogram value (bin content) at that point.
        '''
        assert self.dim() is 1, 'rebin only works for 1D histogram so far.'
        self = histogram(self.grid(), bins=bins, range=range, weights=self)

    def mergebins(self, nbins):
        '''
        nbins = integer greater than one

        merges the contents of a number of sequential bins (nbins)
        into a single bin, through the whole range of the histogram
        and returns a new histogram with fewer bins (at most half).
        '''
        raise Exception('histogram.mergebins() not implemented yet!')











def histogram(sample, bins=None, range=None, **kwargs):
    '''
    wrapper around numpy.histogramdd().
    Differences:
        1. order of dimensions goes like: x, y, z
        2. returns a Histogram object

    histograms the sample. Sets the histogram's dimension
    from the dimension of the sample.

    sample = [x_array, y_array ...]
    bins = [x_bins, y_bins ...]
    range = [ [xmin, xmax], [ymin, ymax] ...]

    x_bins, etc could be an int or a list of the lower bounds of
    each bin, plus the maximum of the highest bin (in which case
    'range' is ignored by numpy.histogramdd)

    **kwargs are passed to numpy.histogramdd()

    returns the Histogram object
    '''
    if type(bins) is type(list()):
        bins = bins[::-1]
    if type(range[0]) is type(list()):
        range = range[::-1]
    else:
        range = [range]
    hist, edges = numpy.histogramdd(sample[::-1], bins=bins, range=range, **kwargs)
    edges = edges[::-1]
    return Histogram(hist, edges)

def apply_attributes(self, obj, plt=None):
    '''
    This applies the labels, titles, and colorbars to itself which
    is of type matplotlib.axes.Axes depending on available attributes
    of
    '''
    cb = None

    if hasattr(self, 'set_xlabel'):
        label = getattr(obj, 'xlabel', False)
        if label:
            self.set_xlabel(label)

    if hasattr(self, 'set_ylabel'):
        label = getattr(obj, 'ylabel', False)
        if label:
            self.set_ylabel(label)

    if hasattr(self, 'set_zlabel'):
        label = getattr(obj, 'zlabel', False)
        if label:
            self.set_zlabel(label)

    if hasattr(self, 'set_title'):
        label = getattr(obj, 'title', False)
        if label:
            self.set_title(label)

    if not plt is None:
        if hasattr(plt, 'autoscale_None'):
            drawcb = getattr(obj, 'colorbar', True)
            if drawcb:
                cb = self.figure.colorbar(plt, ax=self)
                cb_label = getattr(obj, 'cb_label', False)
                if cb_label:
                    cb.set_label(cb_label)

    return cb

matplotlib.axes.Axes.apply_attributes = apply_attributes


def pad_extent(extent, hpad=0.05, vpad=0.05):
    hpadding = hpad * (extent[1] - extent[0])
    vpadding = vpad * (extent[3] - extent[2])

    xlim = [extent[0]-hpadding, extent[1]+hpadding]
    ylim = [extent[2], extent[3]+vpadding]
    if ylim[0] < 0:
        ylim[0] = ylim[0] - vpadding
    return [xlim[0], xlim[1], ylim[0], ylim[1]]

def plothist(self, hist, ymin=0, range=None, **kwargs):
    '''
    axes.Axes.plothist

    ymin and range are passed to Histogram.aspolygon()

        **kwargs are passed to the following matplotlib methods

        for 1D histogram:
            patches.PathPatch()

        for 2D histogram:
            axes.Axes.imshow()
    '''

    if hist.dim() is 1:
        if not 'edgecolor' in kwargs:
            kwargs['edgecolor'] = 'none'

        points, extent = hist.aspolygon(ymin=ymin, range=range)
        points += [points[0]]
        codes = [matplotlib.path.Path.MOVETO] \
            + [matplotlib.path.Path.LINETO]*(len(points) - 3) \
            + [matplotlib.path.Path.MOVETO, matplotlib.path.Path.CLOSEPOLY]

        poly = matplotlib.patches.PathPatch(matplotlib.path.Path(points, codes), **kwargs)

        #print 'vars(poly):', vars(poly)
        #print 'vars(poly._path):', vars(poly._path)
        self.add_patch(poly)

        xmin, xmax, ymin, ymax = pad_extent(extent, hpad=0)
        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)

        self.apply_attributes(hist)

        return (poly, None)

    if hist.dim() is 2:
        ### for 2D histograms, the origin must always be lower
        ### but interpolation can be specified to something
        ### other than nearest.
        if not kwargs.has_key('interpolation'):
            kwargs['interpolation'] = 'nearest'
        if not kwargs.has_key('aspect'):
            kwargs['aspect'] = 'auto'
        plt = self.imshow(
            hist,
            extent = hist.extent(),
            origin = 'lower',
            **kwargs)
        cb = self.apply_attributes(hist, plt)
        return (plt, cb)

matplotlib.axes.Axes.plothist = plothist

def plothist(self, hist, **kwargs):
    '''
    figure.Figure.plothist

    plots a histogram onto the figure

    **kwargs are passed to
        axes.Axes.plothist()
    '''

    ax = self.add_subplot(1,1,1)
    plt, cb = ax.plothist(hist, **kwargs)
    return (ax, plt, cb)

matplotlib.figure.Figure.plothist = plothist

def plothist(hist, **kwargs):
    '''
    plothist

    creates a figure using pyplot, then plots histogram onto it.

    These key word arguments are passed to matplotlib.pyplot.figure()
    default for all is None:
        figsize
        top, bottom, left, right, hspace, wspace

    **kwargs are passed to
        figure.Figure.plothist()
    '''

    figsize = kwargs.pop('figsize', None)
    top = kwargs.pop('top', None)
    bottom = kwargs.pop('bottom', None)
    left = kwargs.pop('left', None)
    right = kwargs.pop('right', None)
    hspace = kwargs.pop('hspace', None)
    wspace = kwargs.pop('wspace', None)
    spp = matplotlib.figure.SubplotParams(top=top, bottom=bottom, left=left, right=right, hspace=hspace, wspace=wspace)
    fig = matplotlib.pyplot.figure(figsize=figsize, subplotpars=spp)
    ax, plt, cb = fig.plothist(hist, **kwargs)
    return (fig, ax, plt, cb)

def overlay(self, hist, range=None, shift_axes=True, **kwargs):
    '''
    axes.Axes.overlay

    overlays a histogram on an axes that is already drawn (self).

    range = [xmin, xmax]
    '''
    if not 'edgecolor' in kwargs:
        kwargs['edgecolor'] = 'none'

    points, extent = hist.aspolygon(range=range)
    points += [points[0]]
    codes = [matplotlib.path.Path.MOVETO] \
        + [matplotlib.path.Path.LINETO]*(len(points) - 3) \
        + [matplotlib.path.Path.MOVETO, matplotlib.path.Path.CLOSEPOLY]

    poly = matplotlib.patches.PathPatch(matplotlib.path.Path(points, codes), **kwargs)

    self.add_patch(poly)

    if shift_axes:
        ax_xlim = self.get_xlim()
        ax_ylim = self.get_ylim()
        poly_ext = pad_extent(extent)
        if hist.dim() > 1:
            self.set_xlim(
                min(ax_xlim[0], poly_ext[0]),
                max(ax_xlim[1], poly_ext[1]) )
        self.set_ylim(
            min(ax_ylim[0], poly_ext[2]),
            max(ax_ylim[1], poly_ext[3]) )

    return poly

matplotlib.axes.Axes.overlay = overlay


def cmap_powerlaw_adjust(cmap, a):
    '''
    returns a new colormap based on the one given
    but adjusted via power-law:

    newcmap = oldcmap**a
    '''
    if a < 0.:
        return cmap
    cdict = copy.copy(cmap._segmentdata)
    fn = lambda x : (x[0]**a, x[1], x[2])
    for key in ('red','green','blue'):
        cdict[key] = map(fn, cdict[key])
        cdict[key].sort()
        assert (cdict[key][0]<0 or cdict[key][-1]>1), "Resulting indices extend out of the [0, 1] segment."
    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)

def cmap_center_adjust(cmap, center_ratio):
    '''
    returns a new colormap based on the one given
    but adjusted so that the old center point higher
    (>0.5) or lower (<0.5)
    '''
    if not (0. < center_ratio) & (center_ratio < 1.):
        return cmap
    a = math.log(center_ratio) / math.log(0.5)
    return cmap_powerlaw_adjust(cmap, a)

def cmap_center_point_adjust(cmap, range, center):
    '''
    converts center to a ratio between 0 and 1 of the
    range given and calls cmap_center_adjust(). returns
    a new adjusted colormap accordingly
    '''
    if not ((range[0] < center) and (center < range[1])):
        return cmap
    return cmap_center_adjust(cmap, abs(center - range[0]) / abs(range[1] - range[0]))

def cmap_center_at_zero(cmap, hist):
    '''
    returns a new colormap where the midpoint of the given colormap
    is now at the zero point of the histogram. This will only work for
    histograms that span above and below zero, otherwise the colormap
    remains unchanged.
    '''
    return cmap_center_point_adjust(cmap, (numpy.min(hist), numpy.max(hist)), 0.)
