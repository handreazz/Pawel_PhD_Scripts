
pdb_file='/net/casegroup2/u2/pjanowsk/Phenix/test100/4hs2/4phenix_4hs2_minall.pdb'

import iotbx.pdb
m=iotbx.pdb.input(file_name=pdb_file)
xrs=m.xray_structure_simple()
scatterers = xrs.scatterers()
site_symmetry_table = xrs.site_symmetry_table()
print site_symmetry_table.n_special_positions()
# for i in site_symmetry_table.special_position_indices(): print i
# import code; code.interact(local=dict(globals(), **locals()))


import iotbx.pdb
pdb_inp = iotbx.pdb.input(file_name=pdb_file)
pdb_hierarchy = pdb_inp.construct_hierarchy()
# pdb_hierarchy.atoms().reset_i_seq()
xrs = pdb_hierarchy.extract_xray_structure(crystal_symmetry = pdb_inp.crystal_symmetry())
# sites_cart=xrs.sites_cart()
# scatterers = xrs.scatterers()
site_symmetry_table = xrs.site_symmetry_table()
print site_symmetry_table.n_special_positions()
# for i in site_symmetry_table.special_position_indices(): print i
# import code; code.interact(local=dict(globals(), **locals()))




from mmtbx import monomer_library
import mmtbx.monomer_library.server
import mmtbx.monomer_library.pdb_interpretation
mon_lib_srv = monomer_library.server.server()
ener_lib = monomer_library.server.ener_lib()
processed_pdb_file = monomer_library.pdb_interpretation.process(
  mon_lib_srv    = mon_lib_srv,
  ener_lib       = ener_lib,
  file_name      = pdb_file,
  raw_records    = None,
  force_symmetry = True)
grm = processed_pdb_file.geometry_restraints_manager(
  show_energies = False,
  plain_pairs_radius = 5.0,
  )
site_symmetry_table = grm.site_symmetry_table
print site_symmetry_table.n_special_positions()
# for i in site_symmetry_table.special_position_indices(): print i
# import code; code.interact(local=dict(globals(), **locals()))