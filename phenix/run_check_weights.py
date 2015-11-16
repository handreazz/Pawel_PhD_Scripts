from __future__ import division
import iotbx.pdb
import sys
import mmtbx.f_model
from libtbx.utils import null_out
from iotbx import reflection_file_utils
import mmtbx.utils
from phenix.refinement import weight_xray_chem
from mmtbx import monomer_library
import mmtbx.monomer_library.server
import mmtbx.model
from scitbx.array_family import flex
import mmtbx.refinement.refinement_flags
import random


if (1):
  random.seed(0)
  flex.set_random_seed(0)

  
def get_fmodel(xrs, hkl_file):
  rfs = reflection_file_utils.reflection_file_server(
    crystal_symmetry = xrs.crystal_symmetry(),
    force_symmetry   = True,
    reflection_files = hkl_file,
    err              = null_out())
  determine_data_and_flags_result = mmtbx.utils.determine_data_and_flags(
    reflection_file_server  = rfs,
    keep_going              = True,
    log                     = null_out())
  f_obs = determine_data_and_flags_result.f_obs
  #r_free_flags = determine_data_and_flags_result.r_free_flags
  print "f-obs labels:", f_obs.info().labels
  #print "r-free-flags labels", r_free_flags.info().labels
  fmodel = mmtbx.f_model.manager(
    xray_structure = xrs,
    f_obs          = f_obs,
    #r_free_flags   = r_free_flags,
    )
  fmodel.update_all_scales()
  print "r_work, r_free: %6.4f %6.4f" % (fmodel.r_work(), fmodel.r_free())
  return fmodel
    
def exercise(args, mean_positive_scale=1):
  processed_args = mmtbx.utils.process_command_line_args(
    args=args, log=null_out())
  use_amber=False
  for arg in args:
    if arg.split('=')[0] == 'use_amber':
      use_amber=arg.split('=')[1]
    if arg.split('=')[0] == 'prmtop':
      prmtop = arg.split('=')[1]
    if arg.split('=')[0] == 'rst7':
      rst7 = arg.split('=')[1]
  mon_lib_srv = monomer_library.server.server()
  ener_lib = monomer_library.server.ener_lib()
  processed_pdb_file = monomer_library.pdb_interpretation.process(
    mon_lib_srv    = mon_lib_srv,
    ener_lib       = ener_lib,
    file_name      = processed_args.pdb_file_names[0],
    raw_records    = None,
    force_symmetry = True)
  geometry = processed_pdb_file.geometry_restraints_manager(
    show_energies = False, plain_pairs_radius = 5.0)
  if use_amber != 'True':
    print "USING EH"
    restraints_manager = mmtbx.restraints.manager(
      geometry = geometry, normalization = True)
  else:
    print "USING AMBER"
    import amber_adaptbx
    import sander
    amber_structs = amber_adaptbx.sander_structs(
              parm_file_name=prmtop,
              rst_file_name=rst7)
    sander.setup(amber_structs.parm,
                   amber_structs.rst.coords,
                   amber_structs.rst.box,
                   amber_structs.inp)
    restraints_manager = mmtbx.restraints.manager(
        geometry      = geometry,
        normalization = True,
        use_amber     = use_amber,
        amber_structs = amber_structs)
  xray_structure = processed_pdb_file.xray_structure()
  xray_structure.scattering_type_registry(table = "wk1995") # is it is X-ray!
  refinement_flags = mmtbx.refinement.refinement_flags.manager(
    individual_sites = True,
    sites_individual = flex.bool(xray_structure.scatterers().size(), True))
  model = mmtbx.model.manager(
    restraints_manager = restraints_manager,
    xray_structure     = xray_structure,
    refinement_flags   = refinement_flags,
    pdb_hierarchy      = processed_pdb_file.all_chain_proxies.pdb_hierarchy)
  fmodel = get_fmodel(hkl_file=processed_args.reflection_files, 
    xrs=xray_structure)
  fmodels = mmtbx.fmodels(fmodel_xray = fmodel)
  result = weight_xray_chem.weight(
    fmodels               = fmodels,
    model                 = model,
    target_weights_params = weight_xray_chem.master_params.extract(),
    macro_cycle           = 0)
  print dir(result)
  w = result.xyz_weights_result
  print dir(w)
  print w.wx, w.w
  
if (__name__ == "__main__"):
  exercise(sys.argv[1:])
  


