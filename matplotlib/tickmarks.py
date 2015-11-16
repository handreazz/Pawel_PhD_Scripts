#! /usr/bin/python
import sys
import os
from numpy import *
import Scientific.IO.NetCDF
from Numeric import * 
from Scientific.IO import NetCDF as Net
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

##name of NetCDF trajectory file
filename='mergtraj_cent.nc'
firstwaterO=9793
watermodelatoms=3
totalwaters=144
frames=12620

##get the coordinates variable of the binary file
file = Net.NetCDFFile(filename, 'r')
coords=file.variables['coordinates']

#~ print coords.shape
#~ print coords [0,0,:]
#~ print coords [0,0,1]
#~ x=coords[:,:,0]
#~ x.shape()
#~ print x
#~ print x.min()
#~ xmax=x.max()
#~ print '%20.20f' %xmax
#~ xl=x.tolist()
#~ print xl
#~ print xl.index(60.8875274658203125)
#~ i=where[x=='60.8875']

###get all of the water coordinates into one array
xcoords=[]
for frame in range(frames): 
	for atom in range(totalwaters):
		xcoords.append(coords[frame,(firstwaterO+(watermodelatoms*atom)),0])

fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.hist(xcoords,500, range=[-20,80], facecolor='blue', alpha=1.00,histtype='stepfilled')

fig.suptitle('Waterchannel cross-section profile (histogram of water positions, 500bins)', fontsize=16)
ax.set_xlabel('x-coordinate (supercell runs from 0-43. 4 unitcells per supercell)')
ax.set_ylabel('count (# of times a water was found at that coordinate')
minorLocator = MultipleLocator(2)
majorLocator = MultipleLocator(10)
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_minor_locator(minorLocator)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(3)
    line.set_markersize(10)
    
for line in ax.xaxis.get_minorticklines():
    line.set_markeredgewidth(2)
    line.set_markersize(5)    

##the next part uses the histogram class (need histogram.py) to color the histogram. Not necessary
from histogram import *
from numpy import random
h1 = histogram(xcoords, bins=500, range=[-20,80])
colors = ['red', 'blue', 'red']
ranges = [[-20,0], [0,43.3], [43.3,80]]
for c, r in zip(colors, ranges):
    plt = ax.overlay(h1, range=r, facecolor=c)
pyplot.savefig("ChannelCross-Section.png")


#~ plt.savefig("ChannelCross-Section.png")
#~ plt.show()	


