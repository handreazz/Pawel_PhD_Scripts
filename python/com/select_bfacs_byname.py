#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
from Scientific.IO import NetCDF as Net
from Bio.PDB import *

####################
# Select b-factors from all b-factors based on atom names
####################

topo='UC.prmtop'
inp_bfacs_file='bfac_RevSymm.txt'
out_bfacs_file='bfac_RevSymm_selected.dat'

allbfacs=genfromtxt(inp_bfacs_file)
selbfacs=[]
A=prmtop(topo)
names=A.Get_AtomNames()


print len(names)
print len(allbfacs)

for i in range(len(names)):
	if names[i]=='C1\'' or names[i]=='C1H':
		selbfacs.append(allbfacs[i])

		


print len(selbfacs)
f=open(out_bfacs_file,'w')
lineno=0
for i in selbfacs:
	lineno+=1
	f.write('%3d %8.2f\n' %(lineno,i))
#~ savetxt(out_bfacs_file,selbfacs,fmt='%8.2f')
