#! /usr/bin/python
import sys
import os
from numpy import *

unitcells=36
residue=5
ss=1 #1=310helix, 2=alphahelix, 6=turn

#~ g=open('dsspall.sum','w')
#~ g.write('310helix content by unitcell\n')
#~ g.write('UC\t R8\t\t 310helixR18\t 310helixChA\t 310helixChB\n')
#~ 
#~ for i in range(1,10):
	#~ print "i=%d" %i
	#~ f=open('ptraj_dssp', 'w')
	#~ f.write('trajin ../rmsf/unitcells/splittrajectories/0'+str(i)+'.nc\n')
	#~ f.write('secstruct out dssp0'+str(i)+'.dat time 2 :1-20\n')
	#~ f.close()
	#~ os.system('ptraj ../rmsf/1UnitCellPrmtop/pep1cell.prmtop <ptraj_dssp')
#~ 
	#~ x=genfromtxt('dssp0'+str(i)+'.dat.sum')
	#~ b=x[residue-1,ss]
	#~ c=x[residue+9,ss]
	#~ d=mean(x[0:10,1])
	#~ e=mean(x[10:19,1])
	#~ g.write('%d\t%5.3f\t\t%5.3f\t\t%5.3f\t\t%5.3f\n' %(i, b, c, d, e))
#~ 
#~ for i in range(10,unitcells+1):
	#~ print "i=%d" %i
	#~ f=open('ptraj_dssp', 'w')
	#~ f.write('trajin ../rmsf/unitcells/splittrajectories/'+str(i)+'.nc\n')
	#~ f.write('secstruct out dssp'+str(i)+'.dat time 2 :1-20\n')
	#~ f.close()
	#~ os.system('ptraj ../rmsf/1UnitCellPrmtop/pep1cell.prmtop <ptraj_dssp')
#~ 
	#~ x=genfromtxt('dssp'+str(i)+'.dat.sum')
	#~ b=x[residue-1,ss]
	#~ c=x[residue+9,ss]
	#~ d=mean(x[0:10,1])
	#~ e=mean(x[10:19,1])
	#~ g.write('%d\t%5.3f\t\t%5.3f\t\t%5.3f\t\t%5.3f\n' %(i, b, c, d, e))
#~ 
#~ g.close()


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

##thicker axes frame
plt.rc('axes',linewidth=3)
# padding for tick labels
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
plt.rc('legend',fontsize=20)
    
fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
data=genfromtxt('dsspall.sum', skip_header=2)

ax.plot(data[:,0], data[:,1],'r-', data[:,0],data[:,2],'b-', linewidth=2.0)
ax.set_xlabel('Unit Cell',fontsize=24, labelpad=10)
ax.set_ylabel('Average 3-10 helix content',fontsize=24, labelpad=10)
ax.autoscale(enable=True, axis='x', tight='True')
st=fig.suptitle('Average 3-10 helix content by unit cell', fontsize=28,y=.95)
ax.legend(["Chain A", "Chain B"],bbox_to_anchor=(0, 0, .999, .999))
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
plt.show()

#plt.savefig("Avg_310content.png")
