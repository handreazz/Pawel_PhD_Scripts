import mmtbx.f_model
from scitbx.array_family import flex
from cctbx import adptbx
import mmtbx.masks
import iotbx.pdb
from libtbx.test_utils import approx_equal
from iotbx import reflection_file_reader

def example():
  # Read in PDB file and get xray_structure object  
  xray_structure = iotbx.pdb.input(
    file_name = "model.pdb").xray_structure_simple()
  # compute Fcalc from atoms
  f_calc_1 = xray_structure.structure_factors(d_min=1.5).f_calc()
  print f_calc_1.indices().size()
  # create mtz file
  mtz_dataset = f_calc_1.as_mtz_dataset(column_root_label="FC1")
  #
  sel = flex.random_bool(f_calc_1.data().size(), 0.5)
  f_calc_2 = f_calc_1.select(sel)
  print f_calc_2.data().size()
  # add data to mtz
  mtz_dataset.add_miller_array(
    miller_array=f_calc_2,
    column_root_label="FC2")
  # write out mtz   
  mtz_object = mtz_dataset.mtz_object()
  mtz_object.write(file_name = "data.mtz")
  #
  f1, f2 = f_calc_1.common_sets(f_calc_2)
  print f1.data().size(), f2.data().size()
  #
  n = flex.sum( flex.abs( flex.abs(f1.data())-flex.abs(f2.data()) ) )
  d = flex.sum(flex.abs(f2.data()))
  print n/d
  #
  miller_arrays = reflection_file_reader.any_reflection_file(
    file_name = "data.mtz").as_miller_arrays()
  ma_2 = None
  for ma in miller_arrays:
    if(ma.info().labels == ['FC2', 'PHIFC2']):
      ma_2 = ma
      break
  print ma_2
  #
  f_obs1 = abs(f_calc_2)
  
  f_obs2 = f_calc_2.customized_copy(data = flex.abs(f_calc_2.data()))
  
  assert approx_equal(f_obs1.data(), f_obs2.data())
  
  fmodel = mmtbx.f_model.manager(
    f_obs = f_obs1,
    r_free_flags = f_obs1.generate_r_free_flags(),
    xray_structure = xray_structure)
  print dir(fmodel)
  print fmodel.r_work()
  print fmodel.r_free()
  #
  x = flex.double([1,2,3,4])
  print x
  print list(x)
  #
  fft_map = f_calc_1.fft_map(resolution_factor = 0.3)
  fft_map.apply_sigma_scaling()
  m1 = fft_map.real_map_unpadded()
  print "m1:", m1
  print fft_map.n_real()
  #
  m2 = m1.deep_copy()
  #
  m3 = m1+m2
  #
  map_coefficients = f_calc_1.structure_factors_from_map(map = m3)
 
  # 
  sf = miller_set.structure_factors_from_map(
    map            = map_data,
    use_scale      = True,
    anomalous_flag = False,
    use_sg         = False)

#See also: exercise_structure_factors_from_map in cctbx/regression/tst_miller.py 
  
  
  
  
#  # make up k_mask = k_sol * exp(-Bsol*ss)
#  ss = 1./flex.pow2(f_calc.d_spacings().data()) / 4.
#  k_mask = mmtbx.f_model.ext.k_mask(ss, 0.35, 50.)
#  # make up overall isotropic scale factor
#  k_overall = flex.double(f_calc.data().size(), 1)
#  # compute Fmask from model
#  f_mask = mmtbx.masks.manager(miller_array = f_calc).shell_f_masks(
#    xray_structure = xray_structure)[0]
#  f_model_data = k_overall * (f_calc.data() + k_mask * f_mask.data())
#  f_model = f_calc.customized_copy(data = f_model_data)

if (__name__ == "__main__"):
  example()
