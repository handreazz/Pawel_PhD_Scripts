from iotbx import pdb
pdb_name = "shaken.pdb"
pdb_inp = pdb.input(file_name=pdb_name)
symm = pdb_inp.crystal_symmetry()
cell = symm.unit_cell()
sg = symm.space_group()
hierarchy = pdb_inp.construct_hierarchy()
model = hierarchy.models()[0]
for chain in model.chains():
    atoms=chain.atoms()
    xyz=atoms.extract_xyz()
    print xyz