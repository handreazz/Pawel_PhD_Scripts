#! /usr/bin/env python
import os
from numpy import *
import argparse 

#======================================================================#
#                                                                      #
#                                                                      #
#                                                                      #
#======================================================================#


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--AsuTopology", help="Amber single ASU topology file")
parser.add_argument("-u", "--UnitCells", help="number of unit cells in crystal")
parser.add_argument("-a", "--ASUs", help="number of asymmetric units per unit cell")
args = parser.parse_args()


#############################
# SETUP                     #
#############################
unitcells=int(args.UnitCells)
asymunits=int(args.ASUs)
topo=args.AsuTopology

######################################
#   Calculate bbone torsions         #
######################################


for i in range(unitcells):
	for j in range(asymunits):
		f=open('ctraj_bkbndih','w')
		f.write('parm %s\n' %topo)
		f.write('trajin ../revsym/RevSym_%02d_%02d.nc\n' %(i+1,j+1))
		f.write('multidihedral phi psi resrange 1-129 out PhiPsi_%02d_%02d.dat\n' %(i+1,j+1))
		f.close()
		os.system('cpptraj <ctraj_bkbndih')
