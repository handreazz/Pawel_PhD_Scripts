import os, sys

import StringIO

from amber_adaptbx import get_candidates

from libtbx import easy_run

ligand_cif_files_added = {}

def run_refine(cmd):
  print
  print cmd
  print
  # assert 0
  ero = easy_run.fully_buffered(command=cmd)
  sout = StringIO.StringIO()
  ero.show_stdout(out=sout)
  outl = sout.getvalue()
  #print outl
  tmp = cmd.split()
  code = tmp[1]
  ligand_cif_files_added.setdefault(code, [])
  error = True
  while error:
    error=False
    if outl.find("No array of R-free flags found.")>-1:
      assert outl.find("refinement.input.xray_data.r_free_flags.generate=True")>-1
      cmd += " refinement.input.xray_data.r_free_flags.generate=True"
      error=True
    elif outl.find("Number of atoms with unknown nonbonded energy type symbols")>-1:
      error = True
      reading=False
      for line in outl.split("\n"):
        #print line
        if reading:
          tmp = line.split()
          ligand_code = line[22:25].strip()
          print 'ligand_code :%s:' % ligand_code
          cif = get_ligand_cif_filename(ligand_code)
          if cif in ligand_cif_files_added[code]:
            error = False
            break
          ligand_cif_files_added[code].append(cif)
          if cif is not None:
            cmd += " %s" % cif
            break
          else:
            error=False
            break
        if line.find("Number of atoms with unknown nonbonded energy type symbols")>-1:
          reading=True
    if error:
      ero = easy_run.fully_buffered(command=cmd)
      sout = StringIO.StringIO()
      ero.show_stdout(out=sout)
      outl = sout.getvalue()
      print outl
  return cmd

def refine_run_complete(preamble):
  geo_filename = "%s.geo" % preamble
  pdb_filename = "%s.pdb" % preamble
  log_filename = "%s.log" % preamble
  if False: # not os.path.exists(geo_filename):
    return False
  else:
    if not os.path.exists(log_filename):
      return False
    else:
      f=file(log_filename, "rb")
      lines = f.readlines()
      del f
      for line in lines:
        if line.find("phenix.refine: finished")>-1:
          return True
  return False

def get_cmd(pdb_file, code=None, amber=True):
  code = pdb_file[:4]
  cmd = "phenix.refine %s %s.mtz" % (pdb_file, code)
  if amber:
    cmd += " topology_file_name=%s.prmtop amber.coordinate_file_name=%s.rst7 use_amber=1" % (code, code)
  return cmd

def fetch_pdb(code):
  if not os.path.exists("%s.pdb" % code):
    cmd = "phenix.fetch_pdb --mtz %s" % code
    easy_run.call(cmd)
  if not os.path.exists("%s.pdb" % code):
    return None
  return "%s.pdb" % code
  
def run_all_tests(code):
  pdb_file = fetch_pdb(code)
  if pdb_file is None: return None
  i=1
  cmd = get_cmd(pdb_file, amber=False)
  cmd += " refinement.target_weights.optimize_xyz_weight=True"
  cmd += " refinement.main.number_of_macro_cycles=10"
  cmd += " serial=%d" % i
  if refine_run_complete("%s_refine_%03d" % (code, i)):
    print '\n\tAlready done %s_refine_%03d' % (code, i)
  else:
    run_refine(cmd=cmd)
  #
  for hydrogens in ["individual",
                    "riding",
                    ]:
    i+=1
    if refine_run_complete("%s_refine_%03d" % (code, i)):
      print 'Already done %s_refine_%03d' % (code, i)
      continue
    cmd = get_cmd(pdb_file)
    cmd += " hydrogens.refine=%s" % hydrogens
    cmd += " refinement.target_weights.optimize_xyz_weight=True"
    cmd += " refinement.main.number_of_macro_cycles=10"
    cmd += " serial=%d" % i
    run_refine(cmd=cmd)

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
  print 'starting'
  for i, code in enumerate(get_candidates.generate_pdb_codes_amber(
      exclude_resname_classes=[
        "other",
        "rna_dna",
        ])):
    
    if only_i is not None and only_i!=i+1: continue
    print '...',i+1, code
    if dry_run: continue


    print 'Running'
    if not os.path.exists(code):
      os.mkdir(code)
    os.chdir(code)
    run_all_tests(code)
    os.chdir("..")

    if only_i is not None: break
    if only_code is not None: break
  
  
if __name__=="__main__":
 run(dry_run=True)
 #run(*tuple(sys.argv[1:]))
  
