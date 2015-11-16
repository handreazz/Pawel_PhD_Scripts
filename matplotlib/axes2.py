#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib.pyplot as plt


trajno=12 #number of trajectories
residuestot=720 #residues in entire supercell
residuesunit=20 #residues in one unit cell
nowaters=4	#no. of water molecules in the 
refatom=7 #sequence no. of residue to which distance measured
water1=721 #no. of first water molecule (this assumes all water molecules are numbered after the peptides)


# padding for tick labels
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
##thicker axes frame
plt.rc('axes',linewidth=4)



fig=plt.figure(figsize=(14, 12))
fig.subplots_adjust(wspace=.45,right=.95, left=.10,top=.95, bottom=.10, hspace=.25)
#~ plt.suptitle('')

k=0
refatom1=refatom+k*residuesunit
ax=plt.subplot(2,1,1)
for i in range(nowaters):
	watatom=water1+k*nowaters+i
	data=genfromtxt('waterdist2/d'+str(refatom1)+'_'+str(watatom)+'.dat')
	x=[]
	y=[]
	for i in range(24001/10):  #this is to get average over each 10 frames (.2ns)
		x.append((data[10*i,0])/10)
		y.append(average(data[10*i:10*i+10,1]))
	plt.plot(x,y,linewidth=4)

	for label in ax.xaxis.get_ticklabels():
		label.set_fontsize(24)
	for label in ax.yaxis.get_ticklabels():
		label.set_fontsize(24)
	plt.title('Unit Cell 1',fontsize=28)
	#plt.xlabel('Time (ns)',fontsize=28)
	#plt.ylabel('Distance from Aib7',fontsize=28)	
	plt.ylim(ymax=35)
	plt.xlim(xmax=500)	#modify to trajectory length
	
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')
	for line in ax.get_xticklines() + ax.get_yticklines():
		line.set_markeredgewidth(4)
		line.set_markersize(10)
	
k=21
refatom1=refatom+k*residuesunit
ax=plt.subplot(2,1,2)
for i in range(nowaters):
	watatom=water1+k*nowaters+i
	data=genfromtxt('waterdist2/d'+str(refatom1)+'_'+str(watatom)+'.dat')
	x=[]
	y=[]
	for i in range(24001/10):  #this is to get average over each 10 frames (.2ns)
		x.append((data[10*i,0])/10)
		y.append(average(data[10*i:10*i+10,1]))
	plt.plot(x,y, linewidth=4)
	#axis label fontsize
	for label in ax.xaxis.get_ticklabels():
		label.set_fontsize(24)
	for label in ax.yaxis.get_ticklabels():
		label.set_fontsize(24)
	#subplot title
	plt.title('Unit Cell 2',fontsize=28)
	#axis label fontsize and padding	
	plt.xlabel('Time (ns)',fontsize=28, labelpad=10)
	plt.ylabel(r'Distance from Aib7 ($\AA$)',fontsize=28, labelpad=10,verticalalignment='bottom')	
	#axis range
	plt.ylim(ymax=35)
	plt.xlim(xmax=500)	#modify to trajectory length
	
	ax.yaxis.set_ticks_position('left')
	ax.xaxis.set_ticks_position('bottom')
	for line in ax.get_xticklines() + ax.get_yticklines():
		line.set_markeredgewidth(4)
		line.set_markersize(10)
	
#~ plt.show()
#~ #plt.savefig('waterdist.png',dpi=1000,facecolor='gray',aspect='auto')
plt.savefig('waterdist_2_poster.png') 
