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
filename='../ptraj/mergtraj_equiv_translated.nc'

#filename='/home/pjanowsk/Case/pepsim/RunCase/WrapWater/mergtraj_waterwrapped_tr.nc'

firstwaterO=9793 #number of first water oxygen
watermodelatoms=3 #number of atoms in water model
totalwaters=144 #total number of water molecules
frames=3242 #frames in trajectory
coordinate=3 # x-coord=0, ycoord=1, z coord=2, a-coord=3, b-coord=4, c-coord=5
##here enter the invU matrix (deorthogonalization matrix) for taking cartesian 
#coordinates into fractional coordinates, ie boxspace
invU=array( [ [ 0.092575448990928, 0.005110941781298, 0.012649310992308],\
           [0.,                  0.061214034829125, 0.031095562758146],\
           [0.,                  0.,                 0.063119390656148] ])


##get the coordinates variable of the binary file
file = Net.NetCDFFile(filename, 'r')
coords=file.variables['coordinates']

###these were some checks of how to work with NetCDF
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
		#if you want fractional coordinate histogram (along a,b or c)
		if coordinate in range(3,6):
			r=array ( coords[frame,(firstwaterO-1+(watermodelatoms*atom))] )
			rfrac=dot(invU,r)
			#print rfrac
			xcoords.append(rfrac[coordinate-3])
		#if you want cartesian coordiante histogram (along x, y, z)
		elif coordinate in range(0,3):
			xcoords.append(coords[frame,(firstwaterO-1+(watermodelatoms*atom)),coordinate])
#print xcoords
print len(xcoords)

###plot histogram of the x-coordinates
fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
#ax.hist(xcoords,500, range=[-1,6], facecolor='blue', alpha=1.00,histtype='stepfilled')
n=ax.hist(xcoords,500, facecolor='blue', alpha=1.00,histtype='stepfilled')
print n[1]
print n[0]
print n[2]
#~ fig.suptitle('Waterchannel cross-section profile (histogram of water positions, 500bins)', fontsize=16)
fig.suptitle('a-coord profile (histogram of water positions, 500bins)', fontsize=16)
#~ ax.set_xlabel('x-coordinate (supercell runs from 0-43.2 4 unitcells per supercell)')
ax.set_xlabel('a-coordinate')
ax.set_ylabel('count (# of times a water was found at that coordinate)')
minorLocator = MultipleLocator(.1)
majorLocator = MultipleLocator(1)
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
#~ from histogram import *
#~ from numpy import random
#~ h1 = histogram(xcoords, bins=500, range=[-3,6])
#~ colors = ['red', 'blue', 'red']
#~ ranges = [[-20,0.0], [0.0,4], [4,20]]
#~ for c, r in zip(colors, ranges):
    #~ plt = ax.overlay(h1, range=r, facecolor=c)
#~ pyplot.savefig("channelProfileY.png")


#plt.savefig("a.png")
plt.show()	


