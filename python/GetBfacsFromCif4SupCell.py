#! /usr/bin/python
import sys
import os
from numpy import *


#####input the following variables
crystalfile=sys.argv[1]
targetfile=sys.argv[2]
totres=20  #total number of residues in asymunit
totasym=36 #total number of asymunits (must be at least the number of asym units in target file)

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
		resnum=int(line[22:26])
		atomname=line[12:16]
		for line2 in p:
			if line2[0:6] != 'ATOM  ':
				continue
			for i in range(totasym):
				if (int(line2[22:26])+(totres*i))==resnum and line2[12:16]==atomname and line2[17:20]!='WAT':
					bfactor=float(line2[60:66])
					f.write(line[0:60]+'%6.2f' %bfactor +line[66:])
				#~ elif int(line2[22:26])==21
					#~ print (int(line2[22:26])+(4*i)+700)
					#~ print line2[
					#~ print 
					#~ line2[17:20]=='WAT':
					#~ print line2[17:20]
				elif (int(line2[22:26])+(4*i)+700)==resnum and line2[12:16]==atomname and line2[17:20]=='WAT':
					bfactor=float(line2[60:66])
					f.write(line[0:60]+'%6.2f' %bfactor +line[66:])
f.close()				
