#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
from Scientific.IO import NetCDF as Net
from Bio.PDB import *


A=prmtop('1rpg_asym.prmtop')
A=prmtop('/home/pjanowsk/York/hairpin/boom/topo.prmtop')
A.names=A.Get_AtomNames()
print len(A.names)
print A.names
L=[]
for type in A.names:
	if 'H' in type:
		continue
	elif 'EP' in type:
		continue
	else:
		L.append(type)
print len(L)
print len(A.Types)


parser=PDBParser()
structure=parser.get_structure('tip','tmp2.pdb')
ats=structure.get_atoms()
c=[]
for at in ats:
	c.append(list(at.get_coord()))
c=array(c)
print shape(c)





