#! /usr/bin/python
import sys
import os
from numpy import *

####
#This program prints a restraint file to add to the equilibration input file.
#It takes the atom number from ambpdb which is a pdb created from the amber crd file
#and the atom bfactor from the pdbfile. For waters, the atom number is calculated
#directly from the number of asym units, number of first water, number of atoms per water.
###


#####input the following variables
scale=float(sys.argv[1]) #scale constraints by this much
AunitAtoms=2020  # number of atoms in asymmetric units
NoAunits=12   #total number of asymmetric units in system
firstwat=26196   #atom number of first water oxygen
wattype=4 #number of atoms in water model
pdbfile='pdbfile'
ambfile='ambfile'

#############################
#read pdb with bfactors: make sure before hand that atom names match
#amber pdb and that residue numbers match amber pdb. (to do this I used
#trim and grep -v to eliminate H atoms and tip4p EW, then cut/pasted the 
#residue number column from the amber pdb). Also, no double atoms, just 
#assymetric unit, etc. Make sure it has the waters too.
####
f=open(pdbfile,'r')
p= [l for l in f.readlines() if l.strip()]
f.close()

#read in amber pdb (eliminate H and EW atoms,
f=open(ambfile,'r')
a = [l for l in f.readlines() if l.strip()]
f.close()

f=open('restraints.txt','w')

#heavy atom restraints
for i in range(NoAunits): 
	addat=AunitAtoms*i  
	print addat
	for line in a: 
		line=line.split()
		if len(line)<=10:
			continue
		else:
			resnum=int(line[4])
			atomname=line[2]
			atomnum=int(line[1])+addat
			for line2 in p:
				line2=line2.split()
				if len(line2)<=10:
					continue
				else:	
					if int(line2[5])==resnum and line2[2]==atomname:
						bfactor=float(line2[10])
						restraint=((2000/bfactor)+25)*scale
						f.write('Restraint for atom %d\n' % atomnum)
						f.write('%.12f\n' % restraint)
						f.write('ATOM %d\n' % atomnum)
						f.write('END\n')

#water restraints
for i in range(NoAunits):
	for line2 in p:
		line2=line2.split()
		if len(line2)<=10:
			continue
		else:
			if line2[3] == 'HOH':
				bfactor=float(line2[10])
				restraint=((2000/bfactor)+25)*scale
				f.write('Restraint for atom %d\n' % firstwat)
				f.write('%.12f\n' % restraint)
				f.write('ATOM %d\n' % firstwat)
				f.write('END\n')
				firstwat=firstwat+wattype	
						
f.write('END\n')
f.close()				
