#! /usr/bin/python
import MDAnalysis.coordinates.DCD
import MDAnalysis.coordinates.DCD as dcd
from numpy import *

x=dcd.DCDReader('mdtest_flexible_yes.dcd')

#unit cell paramters at frame 1
x[1].dimensions

#number of frames
frames=len(x)
n=zeros((frames,6))

#array of unit cell parameters for all frames
for ts in range(frames):
	for i in range(6):
		n[ts,i]=x[ts].dimensions[i]

savetxt('mdtest_felxible_yes_unitcell.txt',n,fmt=['%10.6f','%10.6f','%10.6f','%10.6f','%10.6f','%10.6f'])


p=n/n[0,:]
savetxt('mdtest_felxible_yes_unitcell_proportions.txt',p,fmt=['%10.6f','%10.6f','%10.6f','%10.6f','%10.6f','%10.6f'])


