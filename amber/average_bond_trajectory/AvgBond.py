#! /usr/bin/env python
import os
from numpy import *
from ReadAmberFiles import *
import argparse 

#======================================================================#
#                                                                      #
# Calculate Average structure and find a bond length                   #
#                                                                      #
#======================================================================#


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--AsuTopology", help="Amber single ASU topology file")
parser.add_argument("-pdb", "--AsuPDB", help="Single ASU PDB file")
parser.add_argument("-u", "--UnitCells", help="number of unit cells in crystal")
parser.add_argument("-a", "--ASUs", help="number of asymmetric units per unit cell")
parser.add_argument("-Rm1", help="Suffix for heavy atom rmsd")
parser.add_argument("-Rm2", help="Suffix for backbone atom rmsd")
parser.add_argument("-Rm3", help="Suffix for active site rmsd")
parser.add_argument("-suffix", help="Suffix for output file names")
args = parser.parse_args()


#############################
# SETUP                     #
#############################
unitcells=int(args.UnitCells)
asymunits=int(args.ASUs)
topo=args.AsuTopology
pdb=args.AsuPDB
traj=nc('revsym/RevSym_01_01.nc')
frames=traj.Get_Frames()

###################################
# Calculate asu average structure #
###################################

f=open('ctraj_AvgCoord','w')
f.write('parm %s\n' %topo)
f.write('reference %s\n' %pdb)
for i in range(unitcells):
	for j in range(asymunits):
		#~ if j in [0, 2, 8, 10]:
			#~ continue
		#~ else:
			f.write('trajin revsym/RevSym_%02d_%02d.nc\n' %(i+1,j+1))
f.write('rms reference mass %s\n' %args.Rm2)
f.write('average AvgCoord_%s.rst7 restart \n' %(args.suffix))
f.close()
os.system('cpptraj <ctraj_AvgCoord')
os.system('mv AvgCoord_%s.rst7.1 AvgCoord_%s.rst7' %(args.suffix,args.suffix))

###################################
# Calculate asu rmsd              #
###################################
f=open('ctraj_rmsd','w')
f.write('parm %s\n' %topo)
f.write('reference %s\n' %pdb)
f.write('trajin AvgCoord_%s.rst7\n' %(args.suffix))
f.write('rms reference mass out AvgCoord_rmsd_heavy.dat %s \n' %(args.Rm1))
f.write('rms reference mass out AvgCoord_rmsd_bkbn.dat  %s \n' %(args.Rm2))
f.write('rms reference mass out AvgCoord_rmsd_active.dat  %s \n' %(args.Rm3))
f.close()
os.system('cpptraj <ctraj_rmsd')


###################################
# Calculate bong length           #
###################################
f=open('ctraj_bond','w')
f.write('parm %s\n' %topo)
f.write('reference %s\n' %pdb)
f.write('trajin AvgCoord_%s.rst7\n' %(args.suffix))
f.write('distance :49@N1 :5@O5H out Bond_A38N1_G1O5.dat\n')
f.write('distance :49@H1 :5@O5H out Bond_A38H1_G1O5.dat')
f.close()
os.system('cpptraj <ctraj_bond')
