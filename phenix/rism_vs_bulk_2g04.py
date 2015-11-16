import sys
import iotbx.pdb
from libtbx.utils import null_out
import mmtbx.utils
from cctbx.array_family import flex

#======================================================================#
#                                                                      #
# Return R-values and other statistics given an mtz reflection file,   #
# pdb coordinate file and ccp4 map file.                               #
#                                                                      #
# Usage:                                                               #
#              phenix.python run_2g04.py new.mtz 2g0r.pdb 2g0r.map     #
# Returns:                                                             #
# Prints three sets of statistics. 1: no solvent model. 2: default     #
# Phenix bulk solvent model mask. 3: RISM map treated as if it were    #
# the bulk solvent mask                                                #
#                                                                      #
#======================================================================#

def get_inputs(inputs):
  df = mmtbx.utils.determine_data_and_flags(
    reflection_file_server  = inputs.get_reflection_file_server(),
    log = null_out())
  pdb_inp = iotbx.pdb.input(file_name=inputs.pdb_file_names[0])
  xrs = pdb_inp.xray_structure_simple()
  f_obs = df.f_obs.average_bijvoet_mates()
  f_obs, r_free_flags = f_obs.common_sets(df.r_free_flags)
  fmodel = mmtbx.f_model.manager(
    f_obs          = f_obs,
    r_free_flags   = r_free_flags,
    xray_structure = xrs).resolution_filter(d_min=0.95) # need given map gridding
  return fmodel, xrs
  
def sf_from_map(file_name, miller_array):
  import iotbx.ccp4_map
  map_data = iotbx.ccp4_map.map_reader(file_name=file_name).data.as_double()
  return miller_array.structure_factors_from_map(
    map            = map_data,
    use_scale      = True,
    anomalous_flag = False,
    use_sg         = False)
  
def run(args):
  inputs = mmtbx.utils.process_command_line_args(args = args[0:2])
  fmodel, xrs = get_inputs(inputs=inputs)
  #
  # No solvent model
  #
  print "*"*50, "no scaling"
  print "R-work: %6.4f"%fmodel.r_work()
  fmodel.show(show_header=False, show_approx=False)

  #
  # Default solvent model
  #
  print "*"*50, "default bulk solvent mask"
  fmodel_dc = fmodel.deep_copy()
  fmodel_dc.update_all_scales()
  print "R-work: %6.4f"%fmodel_dc.r_work()
  fmodel_dc.show(show_header=False, show_approx=False)
  #
  # Pawel's map 1
  #
  print "*"*50, "RISM map"
  fmodel_dc = fmodel.deep_copy()
  f_mask=sf_from_map(file_name=args[2], miller_array=fmodel_dc.f_calc())
  fmodel_dc.update_core(f_mask = f_mask)
  fmodel_dc.update_all_scales()
  print "R-work: %6.4f"%fmodel_dc.r_work()
  fmodel_dc.show(show_header=False, show_approx=False)

  print fmodel_dc
  print fmodel_dc.show

if (__name__ == "__main__"):
  run(sys.argv[1:])

