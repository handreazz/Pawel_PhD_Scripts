#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

data=genfromtxt('com_shifts.dat')
frames=5161

#####################################
# GENERAL PLOT SETTINGS             #
#####################################
from matplotlib.font_manager import fontManager, FontProperties
font=FontProperties(size=10)
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20)
colors=['#F86606',\
 '#CC0000', \
 '#F3EF02', \
 '#5DF304', \
 '#4E9A06', \
 '#C4A000', \
 '#729FCF', \
 '#0618F4', \
 '#06EFF4', \
 '#A406F4', \
 '#F4069D', \
 '#936F70']  

########################################################################
###                                                                  ###
### One dimensional histograms of com shifts relative to crystal     ###
###                                                                  ###
########################################################################
fig=plt.figure(figsize=(16, 12))
fig.suptitle('ASU center of mass shifts relative to crystal center of mass, 100bins, 1.4us simulation ', fontsize=16)
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,2,1)
ax.hist(data[:,1],100, range=[-1.5,1.5],facecolor='blue', alpha=1.00,histtype='bar')
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('a-vector')
#~ ax.hist(data[:,1],500, range=[-20,80], facecolor='blue', alpha=1.00,histtype='stepfilled')

ax = fig.add_subplot(2,2,2)
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('b-vector')
ax.hist(data[:,2],100, range=[-1.5,1.5],facecolor='blue', alpha=1.00,histtype='bar')

ax = fig.add_subplot(2,2,3)
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('c-vector')
ax.hist(data[:,3],100, range=[-1.5,1.5],facecolor='blue', alpha=1.00,histtype='bar')

ax = fig.add_subplot(2,2,4)
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('total euclidean distance')
ax.hist(data[:,4],100, range=[-1.5,1.5],facecolor='blue', alpha=1.00,histtype='bar')

for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(3)
    line.set_markersize(10)
for line in ax.xaxis.get_minorticklines():
    line.set_markeredgewidth(2)
    line.set_markersize(5)   
#~ plt.show()
plt.savefig('com_1Dhistogram.png')


########################################################################
###                                                                  ###
### One dimensional histograms of com shifts relative to crystal     ###
### Different color for each ASU                                     ###
###                                                                  ###
########################################################################
fig=plt.figure(figsize=(16, 12))
fig.suptitle('ASU center of mass shifts relative to crystal center of mass, 50bins, 1.4us simulation ', fontsize=16)
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,2,1)
for ASU in range(12):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.hist(datanow[:,1],50, range=[-1.5,1.5],color=colors[ASU], alpha=1.00,histtype='step',linewidth=4,label=str(ASU+1))

plt.legend(bbox_to_anchor=(0, 0, .95, .95),prop=font,ncol=1)
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('a-vector')

ax = fig.add_subplot(2,2,2)
for ASU in range(12):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.hist(datanow[:,2],50, range=[-1.5,1.5],color=colors[ASU], alpha=1.00,histtype='step',linewidth=4,label=str(ASU+1))
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('b-vector')
	
ax = fig.add_subplot(2,2,3)
for ASU in range(12):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.hist(datanow[:,3],50, range=[-1.5,1.5],color=colors[ASU], alpha=1.00,histtype='step',linewidth=4,label=str(ASU+1))
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('c-vector')
	
ax = fig.add_subplot(2,2,4)
for ASU in range(12):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.hist(datanow[:,4],50, range=[-1.5,1.5],color=colors[ASU], alpha=1.00,histtype='step',linewidth=4,label=str(ASU+1))
plt.xlabel('distance from crystal center of mass ($\AA$)')
plt.title('total euclidean distance')	
#~ plt.show()	
plt.savefig('com_1Dhistogram_perASU.png')

########################################################################
###                                                                  ###
### 2D and 3D scatter plots of com shifts relative to crystal        ###
###                                                                  ###
########################################################################
fig=plt.figure(figsize=(16, 12))
fig.suptitle('ASU center of mass shifts relative to crystal center of mass, 100bins, 1.4us simulation ', fontsize=16)
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,2,1)
ax.scatter(data[:,1],data[:,2],c='b',marker='o',s=2,edgecolors='none')
plt.xlabel('a-vector')
plt.ylabel('b-vector')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)

ax = fig.add_subplot(2,2,2)
plt.xlabel('a-vector')
plt.ylabel('c-vector')
ax.scatter(data[:,1],data[:,3],c='b',marker='o',s=2,edgecolors='none')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)

ax = fig.add_subplot(2,2,3)
plt.xlabel('b-vector')
plt.ylabel('c-vector')
ax.scatter(data[:,2],data[:,3],c='b',marker='o',s=2,edgecolors='none')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)

from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(224, projection='3d')
ax.scatter(data[:,1],data[:,2],data[:,3],s=2,c='b',edgecolors='none')
ax.set_xlabel('a vector')
ax.set_ylabel('b vector')
ax.set_zlabel('c vector')
ax.set_zlim3d((-1.5,1.5))
ax.set_ylim3d((-1.5,1.5))
ax.set_xlim3d((-1.5,1.5))

#~ plt.show()
plt.savefig('com_2Dscatter.png')


########################################################################
###                                                                  ###
### 2D and 3D scatter plots of com shifts relative to crystal        ###
### Different color for each ASU                                     ###
###                                                                  ###
########################################################################
fig=plt.figure(figsize=(16, 12))
fig.suptitle('ASU center of mass shifts relative to crystal center of mass, 100bins, 1.4us simulation ', fontsize=16)
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,2,1)
for ASU in reversed(range(12)):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.scatter(datanow[:,1],datanow[:,2],c=colors[ASU],marker='o',s=2,edgecolors='none',label=str(ASU+1))
plt.xlabel('a-vector')
plt.ylabel('b-vector')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)
font=FontProperties(size=14)
plt.legend(bbox_to_anchor=(0, 0, .99, .99),prop=font,ncol=1)

ax = fig.add_subplot(2,2,2)
plt.xlabel('a-vector')
plt.ylabel('c-vector')
for ASU in reversed(range(12)):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.scatter(datanow[:,1],datanow[:,3],c=colors[ASU],marker='o',s=2,edgecolors='none')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)


ax = fig.add_subplot(2,2,3)
plt.xlabel('b-vector')
plt.ylabel('c-vector')
for ASU in reversed(range(12)):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.scatter(datanow[:,2],datanow[:,3],c=colors[ASU],marker='o',s=2,edgecolors='none')
plt.xlim((-1.5,1.5))
plt.ylim((-1.5,1.5))
ax.grid(True)

from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(224, projection='3d')
for ASU in reversed(range(12)):
	datanow=data[ASU*frames:ASU*frames+frames,:]
	ax.scatter(datanow[:,1],datanow[:,2],datanow[:,3],s=2,c=colors[ASU],edgecolors='none')
ax.set_xlabel('a vector')
ax.set_ylabel('b vector')
ax.set_zlabel('c vector')
ax.set_zlim3d((-1.0,1.0))
ax.set_ylim3d((-1.0,1.0))
ax.set_xlim3d((-1.0,1.0))

#~ plt.show()
plt.savefig('com_2Dscatter_perASU.png')

########################################################################
###                                                                  ###
### 2D histogram heatmap of com shifts relative to crystal           ###
###                                                                  ###
########################################################################
fig=plt.figure(figsize=(16, 12))
fig.suptitle('ASU center of mass shifts relative to crystal center of mass, 100bins, 1.4us simulation ', fontsize=16)
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,2,1)
heatmap, xedges, yedges = histogram2d(data[:,1],data[:,2], bins=50)
heatmap=heatmap[:,::-1] #imshow plots the matrix y-axis from top to bottom
plt.imshow(heatmap, interpolation='nearest',extent=[-1.5,1.5,-1.5,1.5])
plt.xlabel('a-vector')
plt.ylabel('b-vector')
plt.colorbar()
ax.grid(True)

ax = fig.add_subplot(2,2,2)
heatmap, xedges, yedges = histogram2d(data[:,1],data[:,3], bins=50)
heatmap=heatmap[:,::-1] #imshow plots the matrix y-axis from top to bottom
plt.imshow(heatmap, interpolation='nearest',extent=[-1.5,1.5,-1.5,1.5])
plt.xlabel('a-vector')
plt.ylabel('c-vector')
plt.colorbar()
ax.grid(True)


ax = fig.add_subplot(2,2,3)
heatmap, xedges, yedges = histogram2d(data[:,2],data[:,3], bins=50)
heatmap=heatmap[:,::-1] #imshow plots the matrix y-axis from top to bottom
plt.imshow(heatmap, interpolation='nearest',extent=[-1.5,1.5,-1.5,1.5])
plt.xlabel('b-vector')
plt.ylabel('c-vector')
plt.colorbar()
ax.grid(True)


from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(224, projection='3d')
ax.scatter(data[:,1],data[:,2],data[:,3],s=2,c='b',edgecolors='none')
ax.set_xlabel('a vector')
ax.set_ylabel('b vector')
ax.set_zlabel('c vector')
ax.set_zlim3d((-1.5,1.5))
ax.set_ylim3d((-1.5,1.5))
ax.set_xlim3d((-1.5,1.5))

#~ plt.show()
plt.savefig('com_2Dhistogram.png')



