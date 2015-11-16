#! /usr/bin/python
import sys
import os
from numpy import *

unitcells=12

g=open('dsspall.sum','w')


#~ for i in range(unitcells):
	#~ print "i=%d" %i
	#~ f=open('ctraj_dssp', 'w')
	#~ f.write('parm ../../4lztUC.prmtop\n')
	#~ f.write('trajin ../revsym/RevSym_%02d_01.nc\n' %(i+1))
	#~ f.write('secstruct out dssp%02d.dat time 2 :1-129\n' %i)
	#~ f.close()
	#~ os.system('cpptraj -i ctraj_dssp')

data=zeros((129,7))
x=genfromtxt('dssp00.dat.sum')
data[:,0]=x[:,0]
for i in range(unitcells):
	x=genfromtxt('dssp%02d.dat.sum' %i)
	#~ print 'dssp%02d.dat.sum' %i
	#~ print "x %s" %(str(x[7,:]))
	#~ print "data %s" %(str(data[7,:]))
	data[:,1:] += x[:,1:]
	#~ print "data %s\n\n" %(str(data[7,:]))
	#~ data[:,1:]/=unitcells
		#~ g.write('%d\t%5.3f\t\t%5.3f\t\t%5.3f\t\t%5.3f\n' %(i, b, c, d, e))		
savetxt(g,data,fmt='%5.2f')
g.close()
most=data[:,1:].argmax(axis=1)
for i in range(len(most)):
	if most[i]==0 and data[i,1]==0:
		most[i]=6
print most

letters = ""
dict1 = {
	0:"b ",
	1:"B ",
	2:"G ",
	3:"H ",
	4:"I ",
	5:"T ",
	6:"0 "
}


for i in range(len(most)):
	letters=letters+dict1[most[i]]
print letters
		
sys.exit()

#~ import matplotlib as mpl
#~ import matplotlib.pyplot as plt
#~ from matplotlib.ticker import MultipleLocator
#~ 
#~ ##thicker axes frame
#~ plt.rc('axes',linewidth=3)
#~ # padding for tick labels
#~ plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
#~ plt.rc('legend',fontsize=20)
    #~ 
#~ fig=plt.figure(figsize=(16, 12))
#~ ax = fig.add_subplot(111)
#~ data=genfromtxt('dsspall.sum', skip_header=2)
#~ 
#~ ax.plot(data[:,0], data[:,3],'r-', data[:,0],data[:,4],'b-', linewidth=2.0)
#~ ax.set_xlabel('Unit Cell',fontsize=24, labelpad=10)
#~ ax.set_ylabel('Average 3-10 helix content (%)',fontsize=24, labelpad=10)
#~ ax.autoscale(enable=True, axis='x', tight='True')
#~ st=fig.suptitle('Average 3-10 helix content by unit cell', fontsize=28,y=.95)
#~ ax.legend(["Chain A", "Chain B"],bbox_to_anchor=(0, 0, .999, .999))
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
#~ #plt.show()
#~ 
#~ plt.savefig("Avg_310content.png")
