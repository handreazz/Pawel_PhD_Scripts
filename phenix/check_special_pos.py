#! /usr/bin/env phenix.python
import iotbx.pdb
import os, sys



base = '1nie'

if os.path.isfile('4phenix_%s_minall.pdb' %base):
  pdb_file = '4phenix_%s_minall.pdb' %base
else:
  pdb_file = '4phenix_%s.pdb' %base


xrs = iotbx.pdb.input(file_name=pdb_file).xray_structure_simple()
site_symmetry_table = xrs.site_symmetry_table()
if site_symmetry_table.n_special_positions() > 0:
  print >> sys.stderr, "WARNING: The following atoms occupy special positions."
  for i in site_symmetry_table.special_position_indices():
    print >> sys.stderr, "  Atom %d" %i

