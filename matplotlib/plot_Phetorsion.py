#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

### Calculate b-factors for each unit cell and plot.
##Modify lines12-15, and 29,30,40,41(selection for RMSD calc.)

plates=10
figname='../Phetorsion_hist.png'
suptitle='Phe_torsion_histograms'
datafiles=[ 'PheA6_phi.txt', 'PheB6_phi.txt', \
'PheA6_psi.txt', 'PheB6_psi.txt', \
'PheA6_ome.txt', 'PheB6_ome.txt', \
'PheA6_1chi.txt', 'PheB6_1chi.txt', \
'PheA6_2chi.txt', 'PheB6_2chi.txt' ]

#~ datafiles=['PheA6_2chi.txt_tmp', 'PheB6_2chi.txt_tmp' ]

fig=plt.figure(figsize=(9, 12))
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
plt.suptitle(suptitle)
for k in range(len(datafiles)):
	ax=plt.subplot(5,2,k+1)
	print datafiles[k]
	data1=genfromtxt(datafiles[k],skip_header=1)
	print shape(data1)
	n, bins, patches = ax.hist(data1[:,1], 50, normed=1, facecolor='blue', alpha=0.75)
	
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
	plt.title(datafiles[k][0:10],fontsize=6)
	plt.xlabel('angle',fontsize=6)
	plt.ylabel('count',fontsize=6)
	minorLocator   = MultipleLocator(5)
	ax.xaxis.set_minor_locator(minorLocator)	
	plt.ylim(0,0.05)
	plt.xlim(-200,200)
#plt.legend(["Simulation", "Experiment"], loc='upper right', bbox_to_anchor=(0, 0, 1, 1),bbox_transform=plt.gcf().transFigure, prop=dict(size='x-small'))
plt.show()
#~ plt.savefig(figname,dpi=300,facecolor='gray',aspect='auto')
		

	



