import os, sys
import StringIO

from libtbx import easy_run

ligand_cif_files_added = {}

def run_refine(cmd, code):
  print cmd
  ero = easy_run.fully_buffered(command=cmd)
  sout = StringIO.StringIO()
  ero.show_stdout(out=sout)
  outl = sout.getvalue()
  #print outl
  tmp = cmd.split()
  #code = tmp[1][-11:-7]
  #print code
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
    print 'error',error
    #print cmd
    if error:
      #easy_run.call(cmd)
      ero = easy_run.fully_buffered(command=cmd)
      sout = StringIO.StringIO()
      ero.show_stdout(out=sout)
      outl = sout.getvalue()
      print outl
  return cmd

def get_cmd(pdb_file):

def run(only_i=None):
  try: only_i=int(only_i)
  except: only_i=None
  code = "1exr"
  i=0
  for hydrogens in ["individual",
                    "riding",
                    ]:
    for adp in [True, False]:
      i+=1
      if only_i is not None and only_i!=i:
        print 'skipping',i,cmd
        continue
      cmd = "phenix.refine 1exr.pdb 1exr.mtz topology_file_name=1exr.prmtop amber.coordinate_file_name=1exr.rst7 use_amber=1"
      cmd += " serial=%d" % i
      run_refine(cmd=cmd,
                 code=code,
        )
      assert 0
    
if __name__=="__main__":
  run(*tuple(sys.argv[1:]))
  
