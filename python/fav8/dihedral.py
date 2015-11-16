#! /usr/bin/python
import sys
import os
from numpy import *
import ls

###############
#This program takes the file containing the dihedral angle over a supertrajectory. 
#It then calculates the average value of that dihedral in each unit cell. 
#################



unitcells=36
frames=120002 #frames per unit cell


def PerUnitCell(textfile): #make new array with set of angles for each UC and mean of each UC in last column
	states=genfromtxt(textfile)
	dih=zeros((frames,unitcells+1)) #additional column for the means
	for i in range(unitcells):		
		ucdih=states[i*frames:(i+1)*frames,1]
		dih[:,i]=ucdih
		dih[i,36]=mean(ucdih)
	savetxt(textfile[:-3]+'new',dih,fmt='%7.3f')

files=ls.ls('ls *txt')
print files
for file in files:
	PerUnitCell(file)



#~ import matplotlib as mpl
#~ import matplotlib.pyplot as plt
#~ from matplotlib.ticker import MultipleLocator

#~ ##thicker axes frame
#~ plt.rc('axes',linewidth=3)
#~ # padding for tick labels
#~ plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
#~ plt.rc('legend',fontsize=20)
#~ #create figure    
#~ fig=plt.figure(figsize=(16, 12))
#~ ax = fig.add_subplot(111)
#~ #import data
#~ data1=genfromtxt('dsspall.sum', skip_header=2)
#~ data2=genfromtxt('avgwaterpercell')
#~ data3=genfromtxt('dihVal18Percent.txt',skip_header=1)
#~ 
#~ #plot data
#~ ax.plot(data1[:,0], data1[:,4],'b-', data3[:,0],data3[:,1],'r-',data2[:,0],data2[:,2],'g-', linewidth=2.0)
#~ #ax.plot(data1[:,0], dih[0:36,36],'b-',)
#~ ax.set_xlabel('Unit Cell',fontsize=24, labelpad=10)
#~ ax.set_ylabel('Percent (%)',fontsize=24, labelpad=10)
#~ ax.autoscale(enable=True, axis='x', tight='True')
#~ #st=fig.suptitle('Average 3-10 helix content and avg. time Val18 bad conformer', fontsize=28,y=.95)
#~ ax.legend(["3-10 helix content (%)", "Time Val18:C-CA-CB-CG1 dih>140deg (%)", "Time in 1|2 water defect (%)"],bbox_to_anchor=(0, 0, .999, .999))
#~ #plt.ylim(0,100)
#~ #plt.xlim(0,120)
#~ #plt.grid(which='both',color='b', linestyle='--', linewidth=.5)
#~ #minorLocator = MultipleLocator(1)
#~ majorLocator = MultipleLocator(1)
#~ ax.xaxis.set_major_locator(majorLocator)
#~ #ax.xaxis.set_minor_locator(minorLocator)
#~ #plt.annotate('Phe4',xy=(26,18), xytext=(26,20),arrowprops=dict(facecolor='black',shrink=.1,width=1,headwidth=5))	
#~ 
#~ ax.yaxis.set_ticks_position('left')
#~ ax.xaxis.set_ticks_position('bottom')
#~ for line in ax.get_xticklines() + ax.get_yticklines():
	#~ line.set_markeredgewidth(4)
	#~ line.set_markersize(10)	
#~ for label in ax.xaxis.get_ticklabels():
	#~ label.set_fontsize(15)
#~ for label in ax.yaxis.get_ticklabels():
	#~ label.set_fontsize(20)
#~ plt.show()
#~ 
#~ #plt.savefig("Avg310vsWatervsVal18Dih.png")
