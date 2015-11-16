#! /usr/bin/python
import sys
import os
from numpy import *

### uses built in ptraj commands to calculate distances between CA atoms.
#In this case two residues in the crystal had C and C1 atoms instead of CA.
#Here calculates average distances over 50ns blocks. modify as necessary.
#First outputs a distance matrix of the pdb file
#The last part calculates the difference between the pdb file and the distance avg.
###




#pdb distance matrix
f=open('ptraj_backbonedist', 'w')
f.write('trajin solvpep.crd\n\n\n')
f.write('matrix dist \':OME@C | :BOC@C1 | @CA\' out dist_pdb.dat')
f.close()
os.system('ptraj solvpep.prmtop <ptraj_backbonedist')

#distance matrices avg over 50ns blocks
#last 50 - 0 ns
f=open('ptraj_backbonedist', 'w')
f.write('trajin solvpep.crd\n\n\n')
for i in range(1012,1262):
	f.write('trajin ../Trajectory/md'+str(i)+'.nc\n\n\n')
f.write('matrix dist \':OME@C | :BOC@C1 | @CA\' out dist_last50to0ns.dat')
f.close()
os.system('ptraj solvpep.prmtop <ptraj_backbonedist')


#last 100-50 ns
f=open('ptraj_backbonedist', 'w')
f.write('trajin solvpep.crd\n\n\n')
for i in range(762,1000):
	f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n')
for i in range(1000,1012):
	f.write('trajin ../Trajectory/md'+str(i)+'.nc\n\n\n')
f.write('matrix dist \':OME@C | :BOC@C1 | @CA\' out dist_last100to50ns.dat')
f.close()
os.system('ptraj solvpep.prmtop <ptraj_backbonedist')


#last 150-100 ns
f=open('ptraj_backbonedist', 'w')
f.write('trajin solvpep.crd\n\n\n')
for i in range(512,762):
	f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n\n\n')
f.write('matrix dist \':OME@C | :BOC@C1 | @CA\' out dist_last150to100ns.dat')
f.close()
os.system('ptraj solvpep.prmtop <ptraj_backbonedist')


#last 200-150 ns
f=open('ptraj_backbonedist', 'w')
f.write('trajin solvpep.crd\n\n\n')
for i in range(262,512):
	f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n\n\n')
f.write('matrix dist \':OME@C | :BOC@C1 | @CA\' out dist_last200to150ns.dat')
f.close()
os.system('ptraj solvpep.prmtop <ptraj_backbonedist')


#diff matrices: difference between the avg distance and the pdb distance
names=['dist_last50to0ns.dat','dist_last100to50ns.dat','dist_last150to100ns.dat'\
,'dist_last200to150ns.dat']

distpdb=genfromtxt('dist_pdb.dat')
for k in names:
	diff=zeros((720,720))
	disttraj=genfromtxt(k)
	for i in range(720):
		for j in range(720):
			diff[i,j]=disttraj[i,j]-distpdb[i,j]
	savetxt('diff'+k[k.index('_'):],diff)
	
	


