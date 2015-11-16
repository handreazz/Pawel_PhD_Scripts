#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


######
#Plot the autocorrelation results of Dave's CompAutoCorr.m
########

#Variables
data1=genfromtxt('c310vH2O')
data2=genfromtxt('c310vVal')
data3=genfromtxt('cValvH2O')

#Matlplotlib rc settings
# padding for tick labels
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
##thicker axes frame
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20)
###set all lines width
plt.rc('lines', linewidth=4)

###################################

#Figure1
#~ fig=plt.figure(figsize=(16, 12))
#~ ax = fig.add_subplot(111)
#~ 
#~ #plot the x-axis diffusion
#~ x=[]
#~ y=[]
#~ for i in range(frames/10):  #this is to get average over each 10 frames (.2ns)
	#~ x.append((data1[10*i,0]))
	#~ y.append(average(data1[10*i:10*i+10,1]))
#~ ax.plot(x,y,'k', linewidth=4)
#~ 
#~ #Linear fit 1
#~ x=range(1,450000,10000) #x-axis range
#~ y=map(lambda i:i*0.0007245+2.578,x) #linear formula
#~ ax.plot(x,y,'r', linewidth=4)
#~ 
#~ #Linear fit 2
#~ x=range(500000,2400000,10000)
#~ y=map(lambda i:i*0.0001965+241.7,x)
#~ ax.plot(x,y,'r', linewidth=4)
#~ 
#~ for label in ax.xaxis.get_ticklabels():
	#~ label.set_fontsize(24)
#~ for label in ax.yaxis.get_ticklabels():
	#~ label.set_fontsize(24)
#~ #plt.title('',fontsize=28)
#~ plt.xlabel('Time (ms)',fontsize=28, labelpad=10)
#~ ax.set_xticklabels([0,0.5,1.0,1.5,2.0,2.5])
#~ plt.ylabel('Mean Square Displacement ($\AA^{2}$)',fontsize=28, labelpad=5)
#~ #plt.ylim(ymax=35)
#~ #plt.xlim(xmax=500)	#modify to trajectory length
#~ 
#~ ax.yaxis.set_ticks_position('left')
#~ ax.xaxis.set_ticks_position('bottom')
#~ for line in ax.get_xticklines() + ax.get_yticklines():
	#~ line.set_markeredgewidth(4)
	#~ line.set_markersize(10)
#~ plt.annotate('Slope=$7.2 x 10^{-4}$',xy=(5000,200), xytext=(340000,200),fontsize=20)
#~ plt.annotate('Slope=$2.0 x 10^{-4}$',xy=(5000,200), xytext=(1500000,475),fontsize=20)
#~ #ax.legend(["peptide", "backbone"],bbox_to_anchor=(0, 0, .95, .2))
#~ 
#~ #plt.show()
#~ plt.savefig('diffusion1.png') 


###############################################

#Figure2
fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)


ax.plot(data1[0:5000],'b', linewidth=4)

ax.plot(data2[0:5000],'r', linewidth=4)

ax.plot(data3[0:5000],'k', linewidth=4)

for label in ax.xaxis.get_ticklabels():
	label.set_fontsize(24)
for label in ax.yaxis.get_ticklabels():
	label.set_fontsize(24)
#plt.title('',fontsize=28)
plt.xlabel('Correlation window size (ns)',fontsize=28, labelpad=10)
ax.set_xticklabels([0,20,40,60,80,100])
plt.ylabel('Avg. Pearson Correlation',fontsize=28, labelpad=10)
plt.ylim((0.6,1.0))
#plt.xlim(xmax=0.5)	#modify to trajectory length

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
for line in ax.get_xticklines() + ax.get_yticklines():
	line.set_markeredgewidth(4)
	line.set_markersize(10)
ax.legend(["$3_{10}$ helix vs. water defect", "$3_{10}$ helix vs. correct Val18 dihedral", "water defect vs. correct Val18 dihedral"],bbox_to_anchor=(0, 0, .995, .25))

#plt.show()
plt.savefig('AutoCorr.pdf') 
