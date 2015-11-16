import os, sys
import shutil

import StringIO

from amber_adaptbx import get_candidates
from amber_adaptbx.command_line import AmberPrep

from libtbx import easy_run
import run_weight

ligand_cif_files_added = {}

def get_amber_input(preamble, ext, raise_exception=False):
  prmtop_filename = "4amber_%s.%s" % (preamble, ext)
  if not os.path.exists(prmtop_filename):
    prmtop_filename = "%s.%s" % (preamble, ext)
  if raise_exception and not os.path.exists(prmtop_filename):
    assert 0
  return prmtop_filename

def amber_prep_complete(preamble):
  prmtop_filename = get_amber_input(preamble,"prmtop")
  rst7_filename = get_amber_input(preamble,"rst7")
  pdb_filename = "4phenix_%s.pdb" % preamble
  if not os.path.exists(prmtop_filename):
    return False
  if not os.path.exists(rst7_filename):
    return False
  if not os.path.exists(pdb_filename):
    return False
##   else:
##     if not os.path.exists(log_filename):
##       return False
##     else:
##       f=file(log_filename, "rb")
##       lines = f.readlines()
##       del f
##       for line in lines:
##         if line.find("phenix.refine: finished")>-1:
##           return True
  return True

def get_mtz_filename(code):
  print os.getcwd()
  for filename in [
      "%s_refine_data.mtz" % code,
      "%s.mtz" % code,
      ]:
    if os.path.exists(filename):
      return filename
  assert 0

def fetch_pdb(code):
  if not os.path.exists("%s.pdb" % code):
    cmd = "phenix.fetch_pdb --mtz %s" % code
    easy_run.call(cmd)
  if not os.path.exists("%s.pdb" % code):
    return None
  return "%s.pdb" % code

def run_all_tests(code, dry_run=False):
  pdb_file = fetch_pdb(code)
  if pdb_file is None: return None
  #
  process_history = "_downloaded"
  if not amber_prep_complete(code):
    print "\n\tRunning AmberPrep\n"
    rc = AmberPrep.run(("%s.pdb" % code, "minimise=amber_h", "redq=True"))
    print 'Substituting Amber PDB file for downloaded file'
    os.rename("%s.pdb" % code, "%s%s.pdb" % (code, process_history))
    shutil.copy(rc, "%s.pdb" % code)
  else:
    print "\n\tAmberPrep already done"
  sys.stdout.flush()

  run_weight.exercise([pdb_file, get_mtz_filename(code)])

def run(only_i=None,
        only_code=None,
        dry_run=False,
        ):
  try: only_i=int(only_i)
  except: only_i=None
  if only_i==0: only_i=None
  if only_i is not None and only_i<0:
    only_i=abs(only_i)
    dry_run=True

  codes = []
  for i, code in enumerate(get_candidates.generate_pdb_codes_amber(
      exclude_resname_classes=[
        "other",
        "rna_dna",
        ])):
  #for i, code in enumerate(["424d",
  #                          "1bzq",
  #                          "3p4g",
  #                          "1ad0",
  #                          #"1aar", # too old and poor
  #                          "1aoj",
  #                          # "1yjp", cell is two small
  #                          ]):
    if code=="3ubk": code = "4lzt"
    #if code=="3ubk": code = "1bzq"
    if only_i is not None and only_i!=i+1: continue
    if only_code is not None and only_code.lower()!=code.lower(): continue
    print '...',i+1, code
    if dry_run: continue

    pd = code[1:3]
    if not os.path.exists(pd):
      os.mkdir(pd)
    os.chdir(pd)
    if not os.path.exists(code):
      os.mkdir(code)
    os.chdir(code)

#    if not os.path.exists("4amber_%s.rst7" % code): 
    run_all_tests(code)

    os.chdir("..")
    os.chdir("..")

    if only_i is not None: break
    if only_code is not None: break
    
if __name__=="__main__":
  args = sys.argv[1:]
  del sys.argv[1:]
  run(*tuple(args))
