import os, sys
import subprocess
import matplotlib.pyplot as plt
from numpy import *

def make_dir(code):
  try:
    os.makedirs(code)
  except OSError:
    if not os.path.isdir(code):
        raise

def dict_n_rfree(file):
  i=0
  with open(file) as f:
    for line in f.readlines():
      print "\nFile %d of 222" %i
      code=line[0:4]
      command='phenix.reflection_file_converter --generate-r-free-flags ' \
              '%s_start.mtz --label="F,SIGF" --mtz=%s_start_rfree' %(code,code)
      print command
      x=subprocess.check_output(command, shell=True)

      command="writedict -in %s_h.oeb -prot %s_start.pdb -out %s_oe " \
              "-planarAniline -nolookup -type 2 2>%s_writedict.log" %(code,code,code,code)
      print command
      x=subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

      make_dir(code)

      i+=1

def get_codes(file):
  codes=[]
  with open(file) as f:
    for line in f.readlines():
      code=line[0:4]
      codes.append(code)
  return codes

def make_ligands_file(codes):
  ofile=open("ligands.txt","w")
  for code in codes:
    ofile.write('%s ' %code)
    with open('%s_oe.cif' %code) as f:
      while True:
        line = f.readline()
        if line.strip() == "_chem_comp.number_atoms_nh":
          while True:
            line = f.readline()
            if line[0] == '#':
              break
            else:
              lig_name=line[0:3]
              n_atoms=int(line.strip().split()[-1])
              ofile.write("%s %3d " %(lig_name, n_atoms))
        else:
          continue
        break
    ofile.write("\n")
  ofile.close()

def get_code_lig_dict(t_range):
  codes = {}
  with open('ligands.txt') as f:
    lines=f.readlines()
    lines=lines[t_range[0]:t_range[1]]
  for line in lines:
    line=line.strip().split()
    code=line[0]
    n_longest_lig=0
    for i,word in enumerate(line):
      if i%2 == 0 and i>0:
        n_atoms=int(word)
        if n_atoms > n_longest_lig:
          n_longest_lig = n_atoms
          longest_lig = line[i-1]
    codes[code] = longest_lig
  return codes

def get_resname_resid(code,f, g):
  ligands={}
  resnames=codes[code].split(',')
  #~ for resname in resnames:
  command= 'mmtbx.afitt %s_oe.pdb %s_oe.cif %s' %(code, code, codes[code])
  print command
  x=subprocess.check_output(command, shell=True)
  print x
  for resname in resnames:
    ligands[resname]=[]
  x=[line for line in x.split('\n') if line]
  for line in x:
    resname=line[0:3]
    id= line.split()[0].split('_',1)[1]
    ligands[resname].append(id)
  print ligands
  f.write('          ')
  g.write('          ')
  for ligand in ligands:
    for instance in ligands[ligand]:
      f.write('%3s_%-5s  ' %(ligand, instance))
      g.write('%3s_%-5s  ' %(ligand, instance))
  f.write('\n')
  g.write('\n')
  return ligands

def file_header(ligands):
  header=[]
  for ligand in ligands:
    for instance in ligands[ligand]:
      header.append('%3s_%-5s' %(ligand, instance))
  return header

def get_energy(pdbfile, code, prefix,scale, ligands, f, header):
  os.chdir(code)
  f.write("sc_%-7s" %prefix)
  command= 'mmtbx.afitt %s ../%s_oe.cif %s' %(pdbfile, code, codes[code])
  print command
  x=subprocess.check_output(command, shell=True)
  x=[line for line in x.split('\n') if line]
  for instance in header:
    for line in x:
      now_instance='%-9s' %line.split()[0]
      if instance == now_instance:
        f.write("%9.4f  " %float(line.split()[2]))

  if scale == 'gnorm':
    gnorms=[]
    for lig in header:
      gnorms.append([])
    with open('%s_grnorm.dat' %(code)) as g:
      for line in g:
        this_lig='%-9s' %line.split()[1].strip(':')
        this_lig_i=header.index(this_lig)
        gnorms[this_lig_i].append(float(line.split()[2]))
      gnorms=asarray(gnorms)
      mean_gnorm=mean(gnorms, axis=1)
      f.write ("mean_gnorm: ")
      for i in mean_gnorm:
        f.write(" %4.2f" %i)
  f.write("\n")
  os.chdir('..')

def get_rfree(logfile, code, prefix,scale, ligands, f, header):
  os.chdir(code)
  f.write("sc_%-7s" %prefix)
  command= 'tail -n 1 %s' %(logfile)
  print command
  x=subprocess.check_output(command, shell=True)
  x=x.split()
  rwork=x[3].strip(',')
  rfree=x[6]
  f.write("%9.4f  " %float(rwork))
  f.write("%9.4f  " %float(rfree))
  f.write("\n")
  os.chdir('..')


def run_initial_refine(code):
  os.chdir(code)
  status=1
  print "Refining: %s " %(code)
  # run refinements
  if not os.path.isfile("%s_10refined_001.pdb" %(code)) or \
    os.stat("%s_10refined_001.pdb" %(code))[6]==0:
    command='phenix.refine ../%s_oe.pdb ' \
            '../%s_start_rfree.mtz ' \
            '../%s_oe.cif ' \
            'output.prefix=%s_10refined '  \
            '--overwrite ' \
            'refinement.main.number_of_macro_cycles=10 '  \
            '--quiet' %(code, code, code, code)
    print command
    try:
      subprocess.check_call(command,shell=True)
    except subprocess.CalledProcessError:
      print "ERROR: %s refinement went wrong." %(code)
      subprocess.call('echo %s_initial >>../wrong1.txt' %code, shell=True)
      status=0
  os.chdir('..')
  return status

def refine(code, scale, ref_args,prefix):
  os.chdir(code)
  status=1
  print "Refining: %s %s" %(code, prefix)
  # run refinements
  if not os.path.isfile("%s_%s_001.pdb" %(code,prefix)) or \
    os.stat("%s_%s_001.pdb" %(code,prefix))[6]==0:
    command='phenix.refine %s_10refined_001.pdb ' \
            '%s_10refined_001.mtz ' \
            '../%s_oe.cif ' \
            'output.prefix=%s_%s '  \
            '--overwrite ' \
            'refinement.main.number_of_macro_cycles=5 '  \
            'use_afitt=True ligand_file=../%s_oe.cif '\
            'afitt.scale=%s ' \
            'ligand_names=%s ' \
            '%s ' \
            '> %s_%s_afitt.log' %(code, code, code, code, prefix,
                                  code, scale, codes[code],ref_args,
                                  code, prefix)
    print command
    try:
      subprocess.check_call(command,shell=True)
    except subprocess.CalledProcessError:
      print "ERROR: %s refinement went wrong." %(code)
      subprocess.call('echo %s >>../wrong1.txt' %code, shell=True)
      status=0
      
  # make grnorm.dat file
  if scale == 'gnorm':
    x=subprocess.call('grep GRNORM %s_%s_afitt.log > %s_grnorm.dat' %(code,prefix,code), shell=True)

  os.chdir('..')
  return status    


#======================================================================#
#REFINEMENTS TO RUN
ref_args_prefix=[['','sc_10_adp_','10'],['use_afitt=False','no_afitt__','20']]

codes={'1p62':'GEO','1hq2':'PH2','1dib':'L34','1c5x':'ESI','1mbi':'IMD',
       '1ukz':'AMQ','1ia1':'TQ3','1yv3':'BIT','1cde':'GAR','1hnn':'SKF',
       '1exa':'394','1hdy':'PYZ','1lrh':'NLA','1frp':'FDP','1sq5':'PAU',
       '1fcx':'184','1fcz':'156','1ive':'ST3','1t40':'ID5','1t9b':'1CS',
       '1meh':'MOA','1coy':'AND','1pbd':'PAB','1mmv':'3AR',
       '1hww':'SWA','1j3j':'CP6','1d3h':'A26'
       }
i=0

for code in codes:
   i+=1
   print "REFINE %d %s" %(i,code)
   import glob
   if glob.glob('%s/done.txt' %code):
     print "%s IS ALREADY DONE.\n" %code
     print("=============================================================\n")
     continue
   filelist = glob.glob("%s/%s_energy*" %(code,code))+\
              glob.glob("%s/%s_sc*" %(code,code))+\
              glob.glob("%s/%s_rfree*" %(code,code))
   for f in filelist:
    os.remove(f)
   make_dir(code)
   f=open('%s/%s_energy.dat' %(code,code), 'w')
   g=open('%s/%s_rfree.dat' %(code,code), 'w')
   ligands=get_resname_resid(code,f,g)
   header=file_header(ligands)
   get_energy('../%s_oe.pdb' %code, code,'deposi    ', 'deposi',ligands, f,header)
   for ref_args, prefix,scale in ref_args_prefix:
     ref_result=refine(code, scale, ref_args, prefix)
     ref_result=True
     if ref_result:
       get_energy("%s_%s_001.pdb" %(code,prefix), code, prefix,scale, ligands, f, header)
       get_rfree("%s_%s_001.log" %(code,prefix), code, prefix,scale, ligands, g, header)
       subprocess.check_call('touch %s/done.txt' %code, shell=True)
   f.close()
   g.close()
   print("=============================================================\n")
