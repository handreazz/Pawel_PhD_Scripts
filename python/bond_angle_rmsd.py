#! /usr/bin/env phenix.python

from amber_adaptbx import bond_angle_rmsd, sander_structs
from chemistry.amber.readparm import AmberParm, Rst7
import iotbx.pdb


amber_structs=sander_structs('/net/casegroup2/u2/pjanowsk/Phenix/refine_4lzt/4lzt.prmtop',
                 '/net/casegroup2/u2/pjanowsk/Phenix/refine_4lzt/4lzt.rst7')

pdb_inp = iotbx.pdb.input(file_name='/net/casegroup2/u2/pjanowsk/Phenix/refine_4lzt/4lzt.pdb')
pdb_hierarchy = pdb_inp.construct_hierarchy()
pdb_hierarchy.atoms().reset_i_seq()
xrs = pdb_hierarchy.extract_xray_structure()
sites_cart=xrs.sites_cart()


print bond_angle_rmsd(amber_structs.parm, sites_cart)


### BELOW IS THE OLD BOND_ANGLE_RMSD THAT REQUIRED SETTING THE COORDS IN THE
### PARM STRUCT
# import sander
# sander.setup(amber_structs.parm,
#                    amber_structs.rst.coords,
#                    amber_structs.rst.box,
#                    amber_structs.inp)
# print bond_angle_rmsd(amber_structs, sites_cart)


# def bond_angle_rmsd(amber_structs, sites_cart):
#   from math import acos, pi, sqrt
#   sander_coords = list(sites_cart.as_double())
#   sander.set_positions(sander_coords)
#   parm = amber_structs.parm
#   parm.LoadRst7(amber_structs.rst)
#
#   #bond rmsd
#   bdev = 0
#   # import code; code.interact(local=dict(globals(), **locals()))
#   # sys.exit()
#   for i, bond in enumerate(parm.bonds_inc_h + parm.bonds_without_h):
#     atom1, atom2 = bond.atom1, bond.atom2
#     dx = atom1.xx - atom2.xx
#     dy = atom1.xy - atom2.xy
#     dz = atom1.xz - atom2.xz
#     contrib = bond.bond_type.req - sqrt(dx*dx + dy*dy + dz*dz)
#     bdev += contrib * contrib
#   nbond = i + 1
#   bdev /= nbond
#   bdev = sqrt(bdev)
#
#   #angle rmsd
#   adev = 0
#   for i, angle in enumerate(parm.angles_inc_h + parm.angles_without_h):
#     atom1, atom2, atom3 = angle.atom1, angle.atom2, angle.atom3
#     a = flex.double([atom1.xx-atom2.xx, atom1.xy-atom2.xy, atom1.xz-atom2.xz])
#     b = flex.double([atom3.xx-atom2.xx, atom3.xy-atom2.xy, atom3.xz-atom2.xz])
#     print angle.angle_type.theteq*180/pi, acos(a.dot(b)/(a.norm()*b.norm()))*180/pi
#     contrib = angle.angle_type.theteq - acos(a.dot(b)/(a.norm()*b.norm()))
#     contrib *= 180/pi
#     adev += contrib * contrib
#   nang = i + 1
#   adev /= nang
#   adev = sqrt(adev)
#
#   return bdev, adev