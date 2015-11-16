#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

### Calculate b-factors for each unit cell and plot.
##Modify lines12-15, and 29,30,40,41(selection for RMSD calc.)

plates=36
#~ figname='../Phetorsion_hist.png'
suptitle='PheB6_2chi_perUC'
datafiles=['PheB6_2chi.new']

#~ datafiles=['PheA6_2chi.txt_tmp', 'PheB6_2chi.txt_tmp' ]

fig=plt.figure(figsize=(12, 9))
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
plt.suptitle(suptitle)
data=genfromtxt(datafiles[0])

for k in range(plates):
	ax=plt.subplot(6,6,k+1)
	#~ import code; code.interact(local=locals())
	n, bins, patches = ax.hist(data[:,k], 50, normed=1, facecolor='blue', alpha=0.75)
	
	#plot of including terminals
	#ax.plot(data1[0:132,1],'b-', data2[0:132,2], 'r-')
	
	#plot without terminals
	#~ data3=vstack((data1[7:56,:],data1[65:114,:]))
	#~ data4=vstack((data2[7:56,:],data2[65:114,:]))
	#~ ax.plot(data3[0:98,1],'b-', data4[0:98,2], 'r-')
		
	for label in ax.xaxis.get_ticklabels():
		label.set_fontsize(4)
	for label in ax.yaxis.get_ticklabels():
		label.set_fontsize(4)
	ax.xaxis.labelpad = 0
	ax.yaxis.labelpad = 0
	plt.title(str(k+1),fontsize=6)
	plt.xlabel('angle',fontsize=6)
	plt.ylabel('count',fontsize=6)
	minorLocator   = MultipleLocator(5)
	ax.xaxis.set_minor_locator(minorLocator)	
	plt.ylim(0,0.05)
	plt.xlim(-200,200)
#plt.legend(["Simulation", "Experiment"], loc='upper right', bbox_to_anchor=(0, 0, 1, 1),bbox_transform=plt.gcf().transFigure, prop=dict(size='x-small'))
plt.show()
#~ plt.savefig(figname,dpi=300,facecolor='gray',aspect='auto')
		

	



