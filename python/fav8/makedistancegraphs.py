#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import copy
import math
import matplotlib
import sys
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

####Create 2D color plots of matrices

####This function rescales the colorbar to be centered at zero.
def cmap_center_at_zero(cmap, array):
	array_range=np.min(array), np.max(array)
	center=0.
	if not ((array_range[0] < center) and (center < array_range[1])):
		return cmap
	center_ratio=abs(center - array_range[0]) / abs(array_range[1] - array_range[0])
	if not (0. < center_ratio) & (center_ratio < 1.):
		return cmap
	a = math.log(center_ratio) / math.log(0.5)
	if a < 0.:
		return cmap
	cdict = copy.copy(cmap._segmentdata)
	fn = lambda x : (x[0]**a, x[1], x[2])
	for key in ('red','green','blue'):
		cdict[key] = map(fn, cdict[key])
		cdict[key].sort()
		assert (cdict[key][0]<0 or cdict[key][-1]>1), "Resulting indices extend out of the [0, 1] segment."
	return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)

###SECTION A
#####Make 2D plots of the cwd matrices whose name satisfies the given criteria (in this case first
#three letters 'big'. Modify which files you want to do
l=os.listdir('.')
#names=['diff_last240to120ns.dat']
#print names
for x in l:
	print x
	#if x[0:5]=='avg1_' or x[0:10]=='bigmatrix_':
	if x[0:5]=='avg1_':
		majorLocator   = MultipleLocator(20)
		fig=plt.figure()
		plt.suptitle(x)
		dist=np.genfromtxt(x)
		ax = fig.add_subplot(111)
		im=plt.imshow(dist,cmap=cmap_center_at_zero(plt.cm.seismic, dist), origin='lower', interpolation='nearest')
		#ax.yaxis.set_major_locator(majorLocator)
		plt.colorbar()
		plt.savefig(x+'.png',dpi=500,facecolor='gray',aspect='auto')
		
		#plt.show()
	else:
		pass
#plt.show()


###SECTION B
#~ ######Make ZOOM 2D plots of the cwd matrices whose name satisfies the given criteria (in this case first
#~ ##three letters not or dbig. Modify which files you want to do and ranges
#~ names=['bigmatrix_last100to50ns']
#~ for x in names:
	#~ if x[0:3]!='xbig' and x[0:4]!='dbig':
		#~ majorLocator   = MultipleLocator(20)
		#~ minorLocator   = MultipleLocator(5)
		#~ fig=plt.figure()
		#~ plt.suptitle('zoom_'+x)
		#~ dis=np.genfromtxt(x)
		#~ 
		#~ ax = fig.add_subplot(121)
		#~ dist=dis[100:150,100:150]
		#~ im=plt.imshow(dist,cmap=cmap_center_at_zero(plt.cm.seismic, dist), extent=(100,150,100,150), origin='lower', interpolation='nearest')
		#~ ax.xaxis.set_major_locator(majorLocator)
		#~ ax.xaxis.set_minor_locator(minorLocator)
		#~ ax.yaxis.set_minor_locator(minorLocator)
		#~ ax.yaxis.set_major_locator(majorLocator)
		#~ #plt.colorbar()
		#~ 
		#~ ax = fig.add_subplot(122)
		#~ dist=dis[0:150,0:150]
		#~ im=plt.imshow(dist,cmap=cmap_center_at_zero(plt.cm.seismic, dist), extent=(0,150,0,150), origin='lower', interpolation='nearest')
		#~ ax.xaxis.set_major_locator(majorLocator)
		#~ ax.xaxis.set_minor_locator(minorLocator)
		#~ ax.yaxis.set_minor_locator(minorLocator)
		#~ ax.yaxis.set_major_locator(majorLocator)
		#~ plt.colorbar()
#~ 
		#~ #plt.savefig('zoom1'+x+'.png',dpi=500,facecolor='gray',aspect='auto')
		#~ 
		#~ #plt.show()
	#~ else:
		#~ pass
#~ plt.show()

###SECTION C
######For the given matrix of the entire system, produces 2D plots of distances between atoms in each unit cell. A separate figure for each unit cell is produced.
#~ names=['bigmatrix_last1200to800ns', 'bigmatrix_last1600to1200ns', 'bigmatrix_last2000to1600ns', 'bigmatrix_last2400to2000ns','bigmatrix_last400to0ns','bigmatrix_last800to400ns'] #name of matrix
#~ cells=36 		 #number of unit cells in the system
#~ residues=20	     #number of residues in each unit cell
#~ 
#~ for x in names:
	#~ os.system('mkdir -p d'+x)
	#~ dist=np.genfromtxt(x)
	#~ for i in range(36):
		#~ j=i*residues
		#~ dist1=dist[j:j+residues,j:j+residues]
		#~ plt.figure()
		#~ im=plt.imshow(dist1,cmap=cmap_center_at_zero(plt.cm.seismic, dist1), origin='lower', interpolation='nearest')
		#~ plt.title(x+'_'+str(i+1))
		#~ plt.colorbar()
		#~ plt.savefig('d'+x+'/'+x+'_'+str(i+1)+'.png',dpi=500,facecolor='gray',aspect='auto')

###SECTION D
######For the given matrix of the entire system, produces 2D plots of distances between atoms in each unit cell on one sheet.
#names=['bigmatrix_last200to150ns', 'diff_last120to0ns.dat', 'diff_last360to240ns.dat', 'diff_last480to360ns.dat'] #name of matrix
import commands
names = commands.getoutput("ls bigmatrix*ns")
names.split()
cells=36 		 #number of unit cells in the system
residues=20	     #number of residues in each unit cell

for x in names.split():
	print x
	dist=np.genfromtxt(x)
	fig=plt.figure()
	fig.subplots_adjust(wspace=0,right=1, left=0,top=.93, bottom=.05, hspace=.35)
	for i in range(36):
		j=i*residues
		dist1=dist[j:j+residues,j:j+residues]
		ax=plt.subplot(6,6,i+1)
		im=plt.imshow(dist1,cmap=cmap_center_at_zero(plt.cm.seismic, dist1), origin='lower', interpolation='nearest')
		plt.title(str(i+1),fontsize=4)
		for label in ax.xaxis.get_ticklabels():
			label.set_fontsize(4)
		for label in ax.yaxis.get_ticklabels():
			label.set_fontsize(4)
		fig.patch.set_color('gray')
	plt.colorbar()
	plt.suptitle(x)
	plt.savefig(x+'.png',dpi=1000,facecolor='gray',aspect='auto')
#plt.show()

##This code is just to do a quick graph of the data in names
		#plt.figure()
		#dist=np.genfromtxt(x)
		#im=plt.imshow(dist,cmap=cmap_center_at_zero(plt.cm.seismic, dist), origin='lower', interpolation='nearest')
		#plt.title(x)
		#plt.colorbar()
		#plt.savefig(x+'.png',dpi=500,facecolor='gray',aspect='auto')
