#! /usr/bin/python
import sys
import os
from numpy import *

#Calculate the average water state of each unit cell from the "water distribution" file in ChannelWater (saved in avgwaterpercell). Then plot that and the average content of a given secondary structure for each unit cell (obtained from the dsspall.sum file that was made by ptraj.
#Note that the average water state will be for the cell "in front" of the crystal cells the water belongs to. This is in lines 13-16.

states=genfromtxt('../ChannelWater/waterdistribution')

f=open('avgwaterpercell','w')
for i in range(1,37):
	if i%3==1: 
		j=i+2
	elif i%3==0 or i%3==2:
		j=i-1
	avg=mean(states[:,j-1])
	counter=0
	for state in states[:,j-1]:
		if state==1 or state==2:
			counter+=1
	prc=(counter/120002.0)*100
	f.write ('%d\t%3.2f\t%5.2f\n' %(i, avg, prc))
f.close()

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

##thicker axes frame
plt.rc('axes',linewidth=3)
# padding for tick labels
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
plt.rc('legend',fontsize=20)
#create figure    
fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
#import data
data1=genfromtxt('dsspall.sum', skip_header=2)
data2=genfromtxt('avgwaterpercell')

#plot data
ax.plot(data1[:,0], data1[:,4],'b-', data2[:,0],data2[:,1],'r-', linewidth=2.0)
ax.set_xlabel('Unit Cell',fontsize=24, labelpad=10)
ax.set_ylabel('Average 3-10 helix content (%)',fontsize=24, labelpad=10)
ax.autoscale(enable=True, axis='x', tight='True')
st=fig.suptitle('Average 3-10 helix content and average waters per by unit cell', fontsize=28,y=.95)
ax.legend(["3-10 helix content (%)", "Avg. # of waters"],bbox_to_anchor=(0, 0, .999, .999))
#plt.ylim(0,100)
#plt.xlim(0,120)
#plt.grid(which='both',color='b', linestyle='--', linewidth=.5)
#minorLocator = MultipleLocator(1)
majorLocator = MultipleLocator(1)
ax.xaxis.set_major_locator(majorLocator)
#ax.xaxis.set_minor_locator(minorLocator)
#~ plt.annotate('Phe4',xy=(26,18), xytext=(26,20),arrowprops=dict(facecolor='black',shrink=.1,width=1,headwidth=5))	

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
for line in ax.get_xticklines() + ax.get_yticklines():
	line.set_markeredgewidth(4)
	line.set_markersize(10)	
for label in ax.xaxis.get_ticklabels():
	label.set_fontsize(15)
for label in ax.yaxis.get_ticklabels():
	label.set_fontsize(20)
#plt.show()

plt.savefig("Avg310vsWaterState.png")
