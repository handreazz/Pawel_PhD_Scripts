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


################
#Go through the trajectory and for each cell count how many waters that
#cell has in that frame. Make histogram of how many times a certain cell
#has a given number of waters. Also make file "waterdistribution" that 
#stores the matrix where columns are cells and rows are frames and cell(i,j) 
#gives the number of waters in cell j at frame i.

#This script is written assuming that the trajectory is centered at the origin so that if 
#the coordinates are transformed into fractional coordinates, the cell boundaries will be at
#successive intergers. To do this, read the readme file in ChannelWater.
###############################

##name of NetCDF trajectory file
filename='../fit.nc'
firstwaterO=9793  #number of first water oxygen in amber prmtop
watermodelatoms=3 #number of atoms per water molecule
totalwaters=144   #total number of water molecules
frames=25901    #frames in trajectory

##here enter the invU matrix (deorthogonalization matrix) for taking cartesian 
#coordinates into fractional coordinates, ie boxspace
invU=array( [ [ 0.092575448990928, 0.005110941781298, 0.012649310992308],\
           [0.,                  0.061214034829125, 0.031095562758146],\
           [0.,                  0.,                 0.063119390656148] ])



##get the coordinates variable of the binary file
file = Net.NetCDFFile(filename, 'r')
coords=file.variables['coordinates']


f=open('waterdistribution', 'w')
g=open('waterdistribution_supcell', 'w')
d = {}  #will store the histogram of states for wrapped
c = {}  #will store the histogram of states for unwrapped
b = {}  #will store the histogram of states for unwrapped alternative method
for frame in range(frames):
	ccount = {} 
	histcells=zeros(36)
	histsupcell=zeros(108)
	at_coords=[]
	n=0
	for atom in range(totalwaters):
		# get fractional coordinates of each atom and save the coords of all the atoms
		# in this frame in at_coords
		r=coords[frame,(firstwaterO-1+(watermodelatoms*atom))]
		at_coords.append(dot(invU,r))
	for j in at_coords:
		#figure out which cell each atome coordinates correspond to
		x=divmod(j[0],1.0)
		y=divmod(j[1],1.0)
		z=divmod(j[2],1.0)
		#This line must be modified according to how PropPDB made the supercell (in this case
		# there was a c propagation 3 times, then a y three times, than an x 4 times)
		#the original unit cell is cell1, than they go on to 36 as well as negative
		cell=(x[0]*9)+(y[0]*3)+(z[0]*1)

		#the next four lines make a ccount histogram of each 
		if cell in ccount:
			ccount[cell] += 1
		else: 
			ccount[cell] =1
		
		#####Another wrapping technique (assuming no water moves more than one supercell over)
		#this technique produces has the disadvantage over the previous technique that it also records
		#all the zero cells, but it has the advantage that it makes a file like "waterdistribution"
		#which is needed for permanencetiems.py
		histsupcell[int(cell+36)]+=1
		############
		
		
		
		#wrapping: waters in negative cells or in cells >36 must be wrapped into the original
		#super cell
		#case for negative
		if cell < 0:
			wrapby=int(cell/36)-1
			cell=int(cell-(wrapby*36))
		#case for positive (>36)
		if cell >= 0:
			wrapby=int(cell/36)
			cell=int(cell-(wrapby*36))
		
		histcells[cell]+=1
	
		
	#make histogram (first two ifs are to see the occurances of the 0 and 8 state)
	# wrapping histogram
	for x in histcells:
		if x==8:
			print ' 8 waters frame '+str(frame)
			print histcells
		if x==0:
			print ' 0 water frame '+str(frame)
			print histcells
		#making the histogram is the next four lines
		if x in d:
			d[x] += 1
		else: 
			d[x]=1
	#no wrapping histogram
	for x in ccount:
		if ccount[x] in c:
			c[ccount[x]] +=1
		else:
			c[ccount[x]]=1

	#########alternative method histogram
	for x in histsupcell:
		if x in b:
			b[x] += 1
		else: 
			b[x]=1	
	for i in histsupcell:
		g.write("%s " % i)
	g.write('\n')

######################################


	#writing the 'waterdistribution' file
	for i in histcells:
		f.write("%s " % i)
	f.write('\n')

f.close()
g.close()
#print histogram
#print c
print d
#print b

#make bar graph		
#~ d={0: 417, 1: 421621, 2: 489806, 3: 307051, 4: 1057258, 5: 1557759, 6: 463877, 7: 21460, 8: 814, 9: 9}

x=d.keys()
y=d.values()

plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)

fig=plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111)
ax.bar(x,y,align='center')

fig.suptitle('Histogram of Unit Cell Water States', fontsize=28, y=.93)
ax.set_xlabel('State (waters in unit cell)',fontsize=24, labelpad=10)
ax.set_ylabel('Count (x10000)', fontsize=24, labelpad=10)
#center tickmarks
z=array(x) 
#~ ax.set_xlim((-1,10))
plt.xticks(z+1/2)

ax.set_yticklabels([0,5,10,15,20,25,30,35,40,45])

for label in ax.get_xticklabels() + ax.get_yticklabels():
	label.set_fontsize(24)

for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(3)
    line.set_markersize(10)
    
#plt.show()
plt.savefig("waterspercell.png")


