import os, sys
import iotbx.pdb


def get_successful_codes():
  with open('filelist.txt') as f:
    codes=[x.strip().split('_')[0] for x in f.readlines()]
  with open('failed.txt') as f:
    failed=[x.strip() for x in f.readlines()]
  codes = [x for x in codes if x not in failed]
  return codes

def get_pdb_residue_names(pdb_file):
  resnames = []
  pdb_inp = iotbx.pdb.input(file_name=pdb_file)
  pdb_hierarchy = pdb_inp.construct_hierarchy()
  for atom_group in pdb_hierarchy.atom_groups():
    if atom_group.resname not in resnames:
      resnames.append(atom_group.resname)
  return resnames

def get_target_ligands(codes):
  target_ligands = dict()
  for code in codes:
    start_resnames= get_pdb_residue_names('%s_start.pdb' %code)
    oe_resnames = get_pdb_residue_names('%s_oe.pdb' %code)
    ligands = [resname for resname in oe_resnames if resname not in start_resnames]
    if len(ligands) != 1:
      print code, ligands
    else:
      target_ligands[code] = ligands[0]
  return target_ligands

def get_tested_ligands(successful_codes):
  tested_ligands = {}
  with open('ligands.txt') as f:
    lines=f.readlines()
  for line in lines:
    line=line.strip().split()
    code=line[0]
    if code not in successful_codes:
      continue
    n_longest_lig=0
    for i,word in enumerate(line):
      if i%2 == 0 and i>0:
        n_atoms=int(word)
        if n_atoms > n_longest_lig:
          n_longest_lig = n_atoms
          longest_lig = line[i-1]
    tested_ligands[code] = longest_lig
  return tested_ligands

def compare_target_tested(target, tested):
  for key in target_ligands:
    if target_ligands[key] != tested_ligands[key]:
      print key, target[key], tested[key]

codes = get_successful_codes()
target_ligands = get_target_ligands(codes)
tested_ligands = get_tested_ligands(codes)
print len(target_ligands)
print len(tested_ligands)
import code; code.interact(local=dict(globals(), **locals()))
compare_target_tested(target_ligands, tested_ligands)








