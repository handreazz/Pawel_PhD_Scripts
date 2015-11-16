#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *


########################################################################
# Commandline to get center of mass of a structure.
# Arguments:
#     argv[1] - parmtop topology
#	  argv[2] - structure. Use pdb, rst7, or nc file.
#     argv[3] - Frame number. Only necessary if netcdf file is used.
# Return:
#	  prints center of mass to terminal
#########################################################################



topo=prmtop(sys.argv[1])
masses=topo.Get_Masses()

if sys.argv[2].split('.')[-1] == 'nc':
	B=nc(sys.argv[2])
	B.coords=B.Get_Traj()
	coords=B.coords[sys.argv[3],:,:]
	print coords.shape

elif sys.argv[2].split('.')[-1] == 'rst7':
	B=rst7(sys.argv[2])
	coords=B.Get_Coords()

elif sys.argv[2].split('.')[-1] == 'pdb':
	B=pdb(sys.argv[2])
	coords=B.Get_Coords()

else:
	sys.exit("Error: file extension not known. Please use nc, rst7 or pdb.")
	
	
com=COM(coords,masses)
print com

