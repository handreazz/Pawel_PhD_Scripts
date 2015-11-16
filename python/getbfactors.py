#! /usr/bin/python
import sys
import os
from numpy import *

#######
# This script gets the bfactors from the pdb file and prints them in the order that they appear in another pdb file, specifically the
# pdb file created from an amber prmtop that has different atom order in each residue. 
##########
#Check if there is a chain column (ambpdb doesn't put one in but original pdbs usually have one
#Check that there is no bfactors greater than 99.99 (if so need to put space between the occupancy column and the bfactor column).
############


#This is the file generated from tleap with the atom order corresponding to the simulation prmtops
gfile='UC_NoH.pdb'
#This is the original crystal pdb with the bfactors, no double occupancy please.
ffile='1rpg_ah.pdb'
noofresidues=126

glines=[]
with open(gfile) as file_:
	for line in file_:
		#~ line=line.strip().split()
		if not line[0:4]=='ATOM':
			continue		
		glines.append(line)

flines=[]
with open(ffile) as file_:
	for line in file_:
		#~ line=line.strip().split()
		if not line[0:4]=='ATOM':
			continue		
		flines.append(line)
		
out=open('1rpg.bfactors','w')

lnum=0
	
for lineg in glines:
	atom=lineg[12:16].strip()
	resid=lineg[22:26].strip()
	for linef in flines:
		if linef[12:16].strip()==atom and linef[22:26].strip()==resid:
			lnum+=1
			out.write('%4d  %6.2f  %4s  %4s \n' %(lnum, float(linef[60:66]),atom, resid))
out.close()

#####################
# Now produce a file with just C-alpha and C1' b-factors
###

out=open('calpha.bfactors','w')
lnum=0
with open('1rpg.bfactors') as file_:
	for line in file_:
		line=line.strip().split()
		if line[2]=='CA' or line[2]=='C1\'':
			lnum+=1
			out.write('%4d  %5.2f  %4s  %4s \n' %(lnum, float(line[1]), line[2], line[3]))
out.close()


#####################
# Now produce a file with an average side chain b-factor for each residue
###


glines=[]
with open('1rpg.bfactors') as file_:
	for line in file_:
		line=line.strip().split()
		glines.append(line)
out=open('sdch.bfactors','w')
lnum=0

for i in range(1,noofresidues+1):
	residue=[x for x in glines if int(x[3])==i]
	bfacs=array([])
	for atom in residue:
		if atom[2] in ['C','O','N','CA']:
				continue
		else:
				bfacs=append(bfacs,float(atom[1]))
	avgbfac=mean(bfacs)
	if isnan(avgbfac):
		continue
	lnum+=1
	out.write('%4d  %6.2f  %4d \n' %(lnum, avgbfac, i))

out.close()

#####################
# Now produce a file with an average b-factor for each entire residue
###


glines=[]
with open('1rpg.bfactors') as file_:
	for line in file_:
		line=line.strip().split()
		glines.append(line)
out=open('meanresidue.bfactors','w')
lnum=0

for i in range(1,noofresidues+1):
	residue=[x for x in glines if int(x[3])==i]
	bfacs=array([])
	for atom in residue:
		bfacs=append(bfacs,float(atom[1]))
	avgbfac=mean(bfacs)
	if isnan(avgbfac):
		continue
	lnum+=1
	out.write('%4d  %6.2f  %4d \n' %(lnum, avgbfac, i))

out.close()

