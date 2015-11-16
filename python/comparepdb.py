#! /usr/bin/env python

import sys
import fileinput
import os

###########################
## This is used to compare two pdb files and will print out atoms in tmp2.pdb
## that are not found in tmp.pdb based on residue name and atom name.
################

g=open('tmp.pdb','r')
#~ g=open('4lzti_noccup.pdb','r')
glines=g.readlines()
g.close()


with open('UC_NoH.pdb') as file_:
#~ with open('4lztUC.pdb') as file_:
    for line in file_:
		#~ line=line.strip().split()
		if not line[0:4]=='ATOM':
			continue
		match=0	
		for line_g in glines:
			#~ line_g=line_g.strip().split()	
			if not line_g[0:4]=='ATOM':
				continue
			else:
				if line_g[12:16].strip()==line[12:16].strip() and line_g[22:26].strip()==line[22:26].strip():
					match=1
		#~ import code; code.interact(local=locals())
		if match==0:
			print line				

