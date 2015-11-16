def run(pdb_file, cif_file):
  from mmtbx.monomer_library import server
  import iotbx
  from mmtbx.monomer_library import pdb_interpretation
  pdb_inp = iotbx.pdb.input(file_name=pdb_file)
  pdb_hierarchy = pdb_inp.construct_hierarchy()
  raw_lines = pdb_hierarchy.as_pdb_string(
    crystal_symmetry=pdb_inp.crystal_symmetry())
  f=file(cif_file, "rb")
  ligand_cif = f.read()
  f.close()
  cif_object = iotbx.cif.model.cif()
  iotbx.cif.reader(input_string=ligand_cif,
                   cif_object=cif_object,
                   strict=False)
  mon_lib_srv = server.server()
  ener_lib = server.ener_lib()                   
  for srv in [mon_lib_srv, ener_lib]:
    srv.process_cif_object(cif_object=cif_object,
                           file_name="LIGAND")
  processed_pdb = pdb_interpretation.process(
    mon_lib_srv,
    ener_lib,
    raw_records=raw_lines)

  geometry_restraints_manager = processed_pdb.geometry_restraints_manager()
 
if (__name__ == "__main__"):
  run(sys.argv[1], sys.argv[2])

