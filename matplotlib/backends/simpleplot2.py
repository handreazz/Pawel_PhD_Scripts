#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
#mpl.use('Agg')
#mpl.use('Ps')
#mpl.use('Pdf')
#mpl.use('Svg')
#mpl.use('Cairo')
#mpl.use('GDK')
#mpl.use('GTKAgg')
#mpl.use('GTK')
#mpl.use('GTKCairo')
#mpl.use('WXAgg')
#mpl.use('WX')
#mpl.use('TkAgg')
#mpl.use('QtAgg')
#mpl.use('Qt4Agg')
#mpl.use('FLTKAgg')
mpl.use('macosx')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
     
x=['AllnotH_Bfactors_Combined.dat', 'AllnotH_200ns_BBRMSD_Bfactors_Combined.dat','test_Split.dat','cif.bfactors']
fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
data1=genfromtxt(x[0])
data2=genfromtxt(x[1])
data3=genfromtxt(x[2])
data4=genfromtxt(x[3])
ax.plot(data1[0:132,0],data1[0:132,1],'g--', data2[0:132,0],data2[0:132,1],'b:', data3[0:132,0],data3[0:132,1],'r-', data4[0:132,0],data4[0:132,2],'k-')
ax.set_xlabel('atoms')
ax.set_ylabel('b-factor')
#ax.autoscale(enable=True, axis='x', tight='True')
#st=fig.suptitle(x[0]+' + '+x[1], fontsize=12)
st=fig.suptitle('Heavy Atom B-Factors (rmsd to all backbone atoms)', fontsize=16)
ax.legend(["Supercell 250ns", "Supercell 200ns", "Unitcell 200ns", "Experimental"],bbox_to_anchor=(0, 0, .95, .98))
#plt.ylim(0,60)
plt.xlim(0,132.5)
#plt.grid(which='both',color='b', linestyle='--', linewidth=.5)
minorLocator = MultipleLocator(2)
majorLocator = MultipleLocator(10)
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_minor_locator(minorLocator)
plt.annotate('Phe4',xy=(26,18), xytext=(26,20),arrowprops=dict(facecolor='black',shrink=.1,width=1,headwidth=5))	
	

plt.show()

#plt.savefig("tGDK.png")
