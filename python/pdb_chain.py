#! /usr/bin/python
import sys
import os
from numpy import *

####
# Add chain labels to for each ASU in the supercell. This is usefull for
# submitting the crystal to pdbe PISA.
####

### SET ARGUMENTS ###
infile_name='4lztSc_centonpdb_nowat.pdb'
outfile_name='4lztSc_centonpdb_nowat_chains.pdb'
Nres=139 # no of residues per chain

########################################################################

labels=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a']

outfile=open(outfile_name,'w')
with open(infile_name) as infile:
	chain=0
	last_res=Nres
	for line in infile:
		if line[0:6] != 'ATOM  ' and line[0:6] != 'HETATM':
			outfile.write(line)
			continue
		if int(line[22:26]) <= last_res:
			outfile.write(line[0:21]+labels[chain]+line[22:])
		else:
			outfile.write(line[0:21]+labels[chain+1]+line[22:])
			last_res=last_res+Nres
			print last_res
			chain=chain+1
			print labels[chain]
outfile.close()
