import os, sys
from iotbx import pdb

def run(filename, verbose=True):
  print "run",filename
  pdb_inp = pdb.input(filename)
  hierarchy = pdb_inp.construct_hierarchy()

  for model in hierarchy.models():
    if verbose: print 'model: "%s"' % model.id
    for chain in model.chains():
      if verbose: print 'chain: "%s"' % chain.id
      for residue_group in chain.residue_groups():
        if verbose: print '  residue_group: resseq="%s" icode="%s"' % (
          residue_group.resseq, residue_group.icode)
        for atom_group_i, atom_group in enumerate(residue_group.atom_groups()):
          if verbose: print '    atom_group: altloc="%s" resname="%s"' % (
            atom_group.altloc, atom_group.resname)

  for model in hierarchy.models():
    if verbose: print 'model: "%s"' % model.id
    for chain in model.chains():
      if verbose: print 'chain: "%s"' % chain.id
      for conformer in chain.conformers():
        print dir(conformer)
        if verbose: print '  conformer: altloc="%s"' % (
          conformer.altloc)
        for residue in conformer.residues():
          if verbose: print '    residue: resname="%s"' % (
            residue.resname)

  for atom_group in hierarchy.atom_groups():
    print atom_group.resname
    for atom in atom_group.atoms():
      print atom.id_str(), atom.quote()

  hierarchy.atoms().reset_serial()


if __name__=="__main__":
  args = sys.argv[1:]
  del sys.argv[1:]
  run(*tuple(args))
