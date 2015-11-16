#! /usr/bin/python
import sys
import os
from numpy import *
import ReadAmberFiles as Raf
import argparse

#######################################################################################
# Calculate rmsd between two pdb files with and without Kabsch alignment.
# Arguments:
#	file1 - name of first pdb file
#	file2 - name of second pdb file
# Return:
#	 For validation prints size of coordinate matrices read from the pdb file.
#    Then prints the rmsd before alignment and the rmsd after alignment
########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("file1", help="name of first pdb file")
parser.add_argument("file2", help="name of second pdb file")
parser.add_argument("-s", "--selection", help="'bbone' or 'all'. Default is all.", default="all")
parser.add_argument("-r", "--residues", help="residue numbers to be included separted by hyphen (eg. 1-12). Defaults to all.", default="all")
args = parser.parse_args()


pdb1=Raf.pdb(args.file1)
pdb2=Raf.pdb(args.file2)

if args.residues=='all':
	print 'Selected all residues'
else:
	residues=pdb1.filter2list(args.residues)
	pdb1.filter(residues,'residueNo')
	pdb2.filter(residues,'residueNo')
	
if args.selection=='all':
	print 'Selected all atoms'
elif args.selection=='bbone':
	print 'Selected C,CA,N atoms only'
	pdb1.filter(['C','CA','N'],'atom_name')
	pdb2.filter(['C','CA','N'],'atom_name')
else:
	sys.exit("Error: selection unknown please use either bbone or all.")
	
coords1=pdb1.Get_Coords()
coords2=pdb2.Get_Coords()


print "Size of %s is %d x %d" %(args.file1, shape(coords1)[0],shape(coords1)[1])
print "Size of %s is %d x %d" %(args.file2, shape(coords2)[0],shape(coords2)[1])

coords2_align=Raf.KabschAlign(coords1, coords2)

rms=Raf.RMSD(coords1,coords2)
rms_align=Raf.RMSD(coords1,coords2_align)

print rms
print rms_align
