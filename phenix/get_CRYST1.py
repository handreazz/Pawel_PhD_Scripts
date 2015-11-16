

import os, sys
from iotbx import pdb

def run(pdb_filename):
  pdb_inp = pdb.input(pdb_filename)
  cryst1=pdb_inp.crystal_symmetry_from_cryst1()
  pdb_hierarchy=pdb_inp.construct_hierarchy()
  xrs = pdb_inp.xray_structure_simple()
  sc=xrs.sites_cart()
  import code; code.interact(local=locals())
  return cryst1
  
if __name__=="__main__":
  pdb_filename='vAla3.pdb'
  run(pdb_filename)
