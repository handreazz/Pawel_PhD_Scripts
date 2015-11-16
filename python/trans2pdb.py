#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *

########################################################################
# This is a script to move the rst7 coordinates of the asym unit or 
# supercell to the original pdb position (tleap translates the coordinates
# so that symmetry operations would not be applicable because of different 
# relative position of the origin. At present need to modify the script
# COM.tcl to have the correct selection (the residue numbers of one asym
# unit. The lines below create one file for the supercell and one for the asym
# unit. Note to modify everything by hand for now.
#
# After doing this you can fit all supercell frames to this or reverse
# symmetry and than fit...
########################################################################

com1=COM_pdb('1rpg_ah.pdb')
com2=COM_pdb('amb_1rpgK.prmtop 1rpgK.rst7')
tvec=com1-com2
f=open("ptraj_translate", 'w')
f.write('trajin 1rpgK.rst7\n')
f.write('translate x %12.7f y %12.7f z %12.7f\n' %(tvec[0],tvec[1],tvec[2]))
f.write('trajout 1rpgK_tr.rst7 restart\n')
f.close()
os.system('ptraj amb_1rpgK.prmtop <ptraj_translate >ptraj.out')
os.system('mv 1rpgK_tr.rst7.1 1rpgK_tr.rst7')


com1=COM_pdb('1rpg_ah.pdb')
com2=COM_pdb('1rpg_asym.prmtop 1rpg_asym.rst7')
tvec=com1-com2
f=open("ptraj_translate", 'w')
f.write('trajin 1rpg_asym.rst7\n')
f.write('translate x %12.7f y %12.7f z %12.7f\n' %(tvec[0],tvec[1],tvec[2]))
f.write('trajout 1rpg_asym_tr.rst7 restart\n')
f.close()
os.system('ptraj 1rpg_asym.prmtop <ptraj_translate >ptraj.out')
os.system('mv 1rpg_asym_tr.rst7.1 1rpg_asym_tr.rst7')
