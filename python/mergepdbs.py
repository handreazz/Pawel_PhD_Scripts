#! /usr/bin/python
import sys
import os
from numpy import *

########################################################################
# pdb produced by tleap does not have b-factors. Take pdb produced by tleap/
# ambpdb (sys.argv[1]) and original pdb with b-factors and create new pdb (out.pdb)
# that merges the two (adds b-factors and occupancies to the ambpdb pdb).
########################################################################


# usage: /home/pjanowsk/c/scripts/python/mergepdbs.py 1exr_ambpdb.pdb 1exr_ah.pdb

#This is the file generated from tleap with the atom order corresponding to the simulation prmtops
gfile=sys.argv[1]
#This is the original crystal pdb with the bfactors, no double occupancy please.
ffile=sys.argv[2]
noofresidues=126

glines=[]
with open(gfile) as file_:
	for line in file_:
		#~ line=line.strip().split()

		glines.append(line)

flines=[]
with open(ffile) as file_:
	for line in file_:
		#~ line=line.strip().split()
		if not line[0:4]=='ATOM':
			continue		
		flines.append(line)
		
out=open('out.pdb','w')

lnum=0
	
for lineg in glines:
	flag=0
	if not lineg[0:4]=='ATOM':
		out.write(lineg)
	else:
		atom=lineg[12:16].strip()
		resid=lineg[22:26].strip()
		for linef in flines:
			if linef[12:16].strip()==atom and linef[22:26].strip()==resid:
				flag=1
				lnum+=1
				out.write('%s%s%s' %(lineg[0:54], linef[54:66],lineg[66:]))
		if flag==0:
			out.write( '%s%s%s' %(lineg[0:54], '  1.00  0.00' ,lineg[66:]) )	
		flag=0
							
out.close()
print lnum

