from iotbx import reflection_file_reader
import sys
import argparse

#======================================================================#
#                                                                      #
# In an mtz file select only the hkl reflections found in a reference  #
# mtz file. Print out new mtz file with only those reflections.        #
#                                                                      #
# Usage:                                                               #
# phenix.python filter_mtz.py -i md_avg_wat.mtz -ic FP \               #
#                             -r viewing/vsexp_001.mtz -rc I-Obs       #
#                             -o out.mtz                               #
#                                                                      #
# v1: pawel janowski, 12.xii.2013                                      #
#                                                                      #
#======================================================================#

def run(mtz_data_file, d_col, mtz_template_file, t_col, mtz_out_file):
  #READ DATA MTZ
  miller_arrays_data = reflection_file_reader.any_reflection_file(file_name =
    mtz_data_file).as_miller_arrays()
  labels=[ma.info().labels[0] for ma in miller_arrays_data]
  try:
    F_data = miller_arrays_data[ labels.index(d_col) ]
  except:
    print "ERROR: column label not found in input data file"
    sys.exit()
  
  #READ TEMPLATE MTZ  
  miller_arrays_template = reflection_file_reader.any_reflection_file(file_name =
    mtz_template_file).as_miller_arrays()
  labels=[ma.info().labels[0] for ma in miller_arrays_template]
  try:
    F_template = miller_arrays_template[ labels.index(t_col) ]  
  except:
    print "ERROR: column label not found in reference template file"
    sys.exit()
  
  #SELECT REFLECTIONS
  #~ print F_template.size()
  #~ print F_data.size()
  F_data, tmp= F_data.common_sets(F_template)
  #~ print tmp.size()
  #~ print F_data.size()
  
  #WRITE NEW MTZ
  mtz_dataset = F_data.as_mtz_dataset(column_root_label="FP")
  mtz_object = mtz_dataset.mtz_object()
  mtz_object.write(file_name=mtz_out_file) 
    
if (__name__ == "__main__"):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog= '''\
Example:
phenix.python filter_mtz.py -i md_avg_wat.mtz -ic FP -r vsexp_001.mtz -rc I-Obs -o out.mtz
''')
  parser.add_argument("-i",  "--mtz_data", help="mtz file to be filtered", default="md_avg.mtz")
  parser.add_argument("-ic", "--data_column", help="column to be filtered", default="FP")
  parser.add_argument("-r",  "--mtz_template", help="mtz reference file", default="exp.mtz")
  parser.add_argument("-rc", "--ref_column", help="reference column", default="FP")
  parser.add_argument("-o",  "--mtz_out", help="name of output mtz file", default="out.mtz")	
  args = parser.parse_args()
  
  if len(sys.argv)==1:
     parser.print_help()
  else:
    run(args.mtz_data, args.data_column, args.mtz_template, args.ref_column, args.mtz_out)
    
