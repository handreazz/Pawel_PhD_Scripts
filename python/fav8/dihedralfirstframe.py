#! /usr/bin/python
import sys
import os
from numpy import *

unitcells=36

g=open('dihedralfirstframe.txt','w')

for i in range(unitcells):
	f=open('ctraj_dihedralfirstframe.txt','w')
	f.write('parm ../solvpep.prmtop\n')
	f.write('trajin ../ptraj/mergtraj_cent.nc 60000 60000 1\n')
	f.write('dihedral :'+str(i*20+18)+'@C :'+str(i*20+18)+'@CA :'+str(i*20+18)+'@CB :'+str(i*20+18)+'@CG1 out tmp.txt\n')
	f.close()
	os.system('cpptraj -i ctraj_dihedralfirstframe.txt')
	x=genfromtxt('tmp.txt', skip_header=1)
	g.write(str(i+1)+'\t'+str(x[1])+'\n')
g.close()

