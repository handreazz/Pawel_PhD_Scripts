#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import copy
import pylab
import matplotlib


def cmap_center_at_zero(cmap, array):
	array_range=np.min(array), np.max(array)
	center=0.
	if not ((array_range[0] < center) and (center < array_range[1])):
		return cmap
	center_ratio=abs(center - array_range[0]) / abs(array_range[1] - array_range[0])
	if not (0. < center_ratio) & (center_ratio < 1.):
		return cmap
	a = pylab.math.log(center_ratio) / pylab.math.log(0.5)
	if a < 0.:
		return cmap
	cdict = copy.copy(cmap._segmentdata)
	fn = lambda x : (x[0]**a, x[1], x[2])
	for key in ('red','green','blue'):
		cdict[key] = map(fn, cdict[key])
		cdict[key].sort()
		assert (cdict[key][0]<0 or cdict[key][-1]>1), "Resulting indices extend out of the [0, 1] segment."
	return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)

#x='../Case/pepsim/analysis/backbonedist/diff_last50to0ns.dat'
#dist=np.genfromtxt(x)
#im=plt.imshow(dist,cmap=cmap_center_at_zero(plt.cm.seismic, dist), origin='lower', interpolation='nearest')
#plt.title(x[x.rindex('/')+1:])
#plt.colorbar()
#plt.gca()
#plt.gcf()
#plt.show()
##plt.savefig("colormaps.ps",dpi=100,facecolor='gray',aspect='auto')
