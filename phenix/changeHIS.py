import os, sys
from iotbx import pdb

def run(filename, verbose=True):
  print "run",filename
  pdb_inp = pdb.input(filename)
  hierarchy = pdb_inp.construct_hierarchy()
  
  
  
  for atom_group in hierarchy.atom_groups():
    if atom_group.resname == 'HIS':
      if int(atom_group.parent().resseq) in [52, 209,31,98,203]:
        atom_group.resname='HIE'
      elif int(atom_group.parent().resseq) in [174,194]:
        atom_group.resname='HID'
      elif int(atom_group.parent().resseq) in [6]:
        atom_group.resname='HIP'

  hierarchy.write_pdb_file(file_name="my_new_ah.pdb",append_end=True,crystal_symmetry=pdb_inp.crystal_symmetry())


if __name__=="__main__":
  args = sys.argv[1:]
  del sys.argv[1:]
  run(*tuple(args))
