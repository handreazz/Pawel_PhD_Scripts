#! /usr/bin/env python
from __future__ import print_function
import os
import numpy as np
import argparse
import ReadAmberFiles as raf

#======================================================================#
#                                                                      #
# Convert cpptraj normal mode file (evecs) to nmd file for viewing of  #
# normal modes in VMD. Requires VMD 1.9.1 or higher.                   #
#                                                                      #
# Arguments:                                                           #
#    -n number of normal modes to include in the nmd file (default=20) #
#    -ipdb name of pdb file (atoms must correspond to the normal modes)#
#    -ievecs evecs normal mode file created by cpptraj                 #
#    -ofile name of output nmd file (default out.nmd)                  #
#                                                                      #
# http://www.csb.pitt.edu/ProDy/index.html#nmwiz                       #
# v1: pawel janowski                                                   #
#                                                                      # 
#======================================================================#  


def run(nmodes, ipdb_name, ievecs_name, ofile_name):
	#Get info from pdb
	ipdb=raf.pdb(ipdb_name)
	name=ipdb_name.rstrip('.pdb')
	atomnames=ipdb.Get_AtomNames()
	resnames=ipdb.Get_ResidueNames()
	resids=ipdb.Get_ResidueNumbers()
	bfactors=ipdb.Get_Bfactors()
	coordinates=ipdb.Get_Coords()
	
	#Write info from pdb to nmd file
	ofile=open(ofile_name, 'w')
	ofile.write('nmwiz_load %s\n' %ofile_name)
	print('name %s' %name, file=ofile)
	print('atomnames ', end="",file=ofile)
	print (*atomnames, file=ofile)
	print('resnames ', end="",file=ofile)
	print (*resnames, file=ofile)
	print('resids ', end="",file=ofile)
	print (*resids, file=ofile)
	print('bfactors ', end="",file=ofile)
	print (*bfactors, file=ofile)
	print('coordinates ', end="", file=ofile)
	print(*["%8.3f " %xyz for atom in coordinates for xyz in atom], end="", file=ofile)
	#This would've been the python2.x way of doing it:
	#~ for atom in coordinates:
		#~ for coordinate in atom:
			#~ ofile.write("%8.3f " %coordinate)
	print ('', file=ofile)
	
	#Get modes from evecs file and write to nmd file
	modes=[i for i in range(5874,5884)]
	print(modes)
	vecfile=open(ievecs_name, 'r')

	line=vecfile.readline()
	count=0
	while True:
		if count==len(modes):break
		if not line:
			break	
		if line[0:5]==' ****':
			line=vecfile.readline()
			mode_number, freq=line.strip().split()
			if int(mode_number) in modes:
				print(mode_number)
				mode=[]
				line=vecfile.readline()
				while line[0:5]!=' ****' and line:
					for i in line.strip().split():
						mode.append(float(i))
					line=vecfile.readline()
				amplitude=(1/float(freq))	
				print('mode %2d %12.10f ' %(int(mode_number), amplitude), end="", file=ofile)
				print(*["%12.5f " %fluc for fluc in mode], end="", file=ofile)
				print ('', file=ofile)		
				count+=1
		else: 
			line=vecfile.readline()

	vecfile.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", help="number of normal modes to include (default=20)", default=20)
	parser.add_argument("-ipdb", help="name of pdb file (atoms must correspond to normal modes")
	parser.add_argument("-ievecs", help="name of evecs file (output of cpptraj diagmatrix)")
	parser.add_argument("-ofile", help="name of nmd file to output (default=out.nmd)", default="out.nmd")
	args = parser.parse_args()
	run(int(args.n), args.ipdb, args.ievecs, args.ofile)
