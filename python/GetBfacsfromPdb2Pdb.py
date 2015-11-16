#! /usr/bin/python
import sys
import os
from numpy import *


#####input the following variables
crystalfile=sys.argv[1]
targetfile=sys.argv[2]


#############################
#This is to get the bfactors from the original cif or pdb file and put them
#the bfactor column of another file. If atoms are in the same order in the
#two files, you can just use cut, but if not use this script. It identifies
#atoms by atomname and residue number.

f=open(crystalfile,'r')
p= [l for l in f.readlines() if l.strip()]
f.close()

#read in amber pdb (eliminate H and EW atoms,
f=open(targetfile,'r')
a = [l for l in f.readlines() if l.strip()]
f.close()

f=open('newfile.pdb','w')


for line in a: 
	
	if line[0:6] != 'ATOM  ':
		f.write(line)
	else:
		check=0
		resnum=int(line[22:26])
		atomname=line[12:16].strip()
		for line2 in p:
			if line2[0:6] != 'ATOM  ':
				continue
			if (int(line2[22:26]))==resnum and line2[12:16].strip()==atomname:
					bfactor=float(line2[60:66])
					f.write(line[0:60]+'%6.2f' %bfactor +line[66:])
					check=+1
		if check>1:
			print "oh boy something is wrong"
			print line				
					
		if check==0:
			f.write(line)
			print line			

f.close()				
