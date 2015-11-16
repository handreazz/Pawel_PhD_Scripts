from libtbx import group_args
import sys, os
import numpy as np
from iotbx import file_reader

pdb_file="5dnb.pdb"
sg='C121'
uc=[10,10,10, 90,90,90]


def get_symm(sg):
  from cctbx_sgtbx_ext import rt_mx
  if sg == 'P212121':
    rot0=rt_mx("x,y,z")
    rot1=rt_mx("-x+1/2,-y,z+1/2")
    rot2=rt_mx("-x,y+1/2,-z+1/2")
    rot3=rt_mx("x+1/2,-y+1/2,-z")
    rt_mx_matrices=(rot0,rot1,rot2,rot3)
  
  elif sg == 'P1211':
    rot0=rt_mx("x,y,z")
    rot1=rt_mx("-x,y+1/2,-z")
    rt_mx_matrices=(rot0,rot1)

  elif sg == 'P121':      
    rot0=rt_mx("x,y,z")
    rot1=rt_mx("-x,y,-z")
    rt_mx_matrices=(rot0,rot1)

  elif sg == 'P222':
    rot0=rt_mx("x,y,z")
    rot1=rt_mx("-x,-y,z")
    rot2=rt_mx("-x,y,-z")
    rot3=rt_mx("x,-y,-z")
    rt_mx_matrices=(rot0,rot1,rot2,rot3)

  elif sg == 'C121':
    rot0=rt_mx("x,y,z")
    rot1=rt_mx("-x,y,-z")
    rot2=rt_mx("x+1/2,y+1/2,z")
    rot3=rt_mx("-x+1/2,y+1/2,-z")
    rt_mx_matrices=(rot0,rot1,rot2,rot3)    
    
  else:
    print "%s not found\n" %sg
    sys.exit()
  
  return rt_mx_matrices



pdb_in = file_reader.any_file(pdb_file).file_object
pdb_hierarchy = pdb_in.construct_hierarchy()
xrs = pdb_in.xray_structure_simple()
rt_mx_matrices = get_symm(sg)
unit_cell = xrs.unit_cell()


import cctbx
from cctbx import uctbx
uc1=cctbx.uctbx.unit_cell(parameters=uc)
#~ print uc1.parameters()
#~ uc1.show_parameters()
#~ print uc1.volume()


symm = pdb_in.crystal_symmetry()
space_group = symm.space_group()

from cctbx.sgtbx import space_group_info
sg='C121'
i=space_group_info(sg)
space_group=i.group()
for rt_mx in space_group.smx() :
  print rt_mx
x,y,z
-x,y,-z



import code; code.interact(local=dict(globals(), **locals()))
