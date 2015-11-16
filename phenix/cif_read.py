#~ from iotbx import cif
#~ cif_object = cif.reader(file_path="Phenix-AFITT/1azm_in.cif", strict=False).model()
#~ import code; code.interact(local=dict(globals(), **locals()))


import os, sys
from mmtbx import monomer_library
import mmtbx.monomer_library.server
mon_lib_srv = monomer_library.server.server()



residue='AZM'



  
  

get_func = getattr(mon_lib_srv, "get_comp_comp_id", None)
if (get_func is not None): 
  ml=get_func(comp_id=residue)
else:  
  ml=mon_lib_srv.get_comp_comp_id_direct(comp_id=residue)
bonds = []
for bond in ml.bond_list:
  bonds.append([bond.atom_id_1, bond.atom_id_2])
for atom1, atom2 in bonds:
  print atom1, atom2
import code; code.interact(local=dict(globals(), **locals()))
