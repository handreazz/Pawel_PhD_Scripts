#! /usr/bin/python
import sys
import os
from numpy import *

###############
#This program takes the file containing the dihedral angle over a supertrajectory. It then calculates the average value of that dihedral in each unit cell. It then plots for each unit cell the average secondary structure content, average water state and average dihedral value.
#Here the dihedral we are looking at is Val18 C-CA-CB-CG1. Because it is often around 180, I wrap all values below zero by adding 360. The problem is if there were to be a dihedral angle of around 0 than that would get split up. A warning will print whenever there is an angle between 20 and -20. 
#The secondary structure content here is 3-10 helix.
#################

unitcells=36
frames=120002 #frames per unit cell
states=genfromtxt('dihVal18.txt')
startframe=60000
endframe=80000
window=endframe-startframe
#~ 
#~ 
dih=zeros((window,unitcells+1)) #additional column for the means

#Will wrap all angles<0 because i'm interested in angle around 180/-180. But to be sure print angles between -20 and 0 to be sure there is not so many of them.
#~ for i in range(shape(states)[0]):
	#~ if states[i,1]<0 and states[i,1]>-20:
		#~ print ("%3.1f \t %3.1f" % ((states[i,0]/120002) , (states[i,1])))

#wrap angles <0
for i in range(shape(states)[0]):
	if states[i,1]<0:
		states[i,1]=states[i,1]+360.0

#make new array with set of angles for each UC and mean of each UC in last column
for i in range(unitcells):
	print i
	ucdih=states[i*frames+startframe:i*frames+startframe+window,1]
	dih[:,i]=ucdih
	dih[i,36]=mean(ucdih)

#~ savetxt('dihVal18.new',dih,fmt='%7.3f')

#calculate percent time spent in angle>140deg and save in new file
f=open('dihVal18Percent_1200_1600.txt','w')
f.write('UC \t % >140\n')
for i in range(unitcells):
	counter=0
	for j in range(shape(dih)[0]):
		if dih[j,i] >140:
			counter+=1
	prc=(counter/float(window))*100
	print prc
	f.write('%d \t %5.2f\n' % (i+1, prc))
f.close()
#~ 
#~ import matplotlib as mpl
#~ import matplotlib.pyplot as plt
#~ from matplotlib.ticker import MultipleLocator
#~ #print dih[0:36,36]
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
