#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
#mpl.use("Agg")
import matplotlib.pyplot as plt

x=['CaRmsf.dat', 'CaRmsdRmsf.dat']
fig=plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
data1=genfromtxt(x[0])
data2=genfromtxt(x[1])
ax.plot(data1[:,0],data1[:,1],'r-', data2[:,0],data2[:,1],'b-')
ax.set_xlabel('residue')
ax.set_ylabel('rmsf')
ax.autoscale(enable=True, axis='x', tight=True)
st=fig.suptitle(x[0]+' + '+x[1], fontsize=12)
plt.show()

#~ plt.savefig("test.png")
