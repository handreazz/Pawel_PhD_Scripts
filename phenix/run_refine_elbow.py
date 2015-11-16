import os, sys
import subprocess
from numpy import *

def get_codes(file):
  codes=[]
  with open(file) as f:
    for line in f.readlines():
      code=line[0:4]
      codes.append(code)
  return codes

def get_code_lig_dict():
  codes = {}
  codes_all_ligands = {}
  with open('ligands.txt') as f:
    lines=f.readlines()
  for line in lines:
    line=line.strip().split()
    code=line[0]
    all_ligands = []
    n_longest_lig=0
    for i,word in enumerate(line):
      if i%2 == 0 and i>0:
        all_ligands.append(line[i-1])
        n_atoms=int(word)
        if n_atoms > n_longest_lig:
          n_longest_lig = n_atoms
          longest_lig = line[i-1]
    codes[code] = longest_lig
    codes_all_ligands[code] = all_ligands
  return codes, codes_all_ligands

def make_elbow_cif(ligand_dict):
  i=0
  for code in ligand_dict:
    print "\nFile %d of %d: %s" %(i, len(ligand_dict), code)
    for lig in ligand_dict[code]:
      print ligand_dict[code]
      command='phenix.elbow --chemical-component %s --opt' %lig
      print command
      try:
        subprocess.check_output(command, shell=True)
      except:
        print "Error: %s %s" %(code, lig)
      subprocess.call("rm %s.pickle %s.pdb %s.options.pickle %s.elbow_opt.xyz"
                      %(lig, lig, lig, lig), shell=True)
      subprocess.call("mv %s.cif %s_%s_elbow.cif" %(lig, code, lig), shell=True )
    i+=1

def make_elbow_cif_from_input_file(ligand_dict, error_codes):
  i=0
  for code in ligand_dict:
    if code in error_codes:
      print "\nFile %d of %d: %s" %(i, len(error_codes), code)
      for lig in ligand_dict[code]:
        print ligand_dict[code]
        command='phenix.elbow %s_oe.pdb --residue %s > elbow_tmp.out' %(code, lig)
        print command
        try:
          subprocess.check_output(command, shell=True)
        except:
          print "Error: %s %s" %(code, lig)
        subprocess.call("rm elbow.%s.%s_oe_pdb.001.pickle elbow.%s.%s_oe_pdb.001.pdb "
                        %(lig, code, lig, code), shell=True)
        subprocess.call("mv elbow.%s.%s_oe_pdb.001.cif %s_%s_elbow.cif" %(lig, code,  code, lig), shell=True )
      i+=1


def refine(code, ref_args,prefix):
  prefix = '%s_%s' %(code, prefix)
  os.chdir(code)
  status=1
  print "Refining: %s" %(prefix)
  if not os.path.isfile("%s_001.pdb" %prefix) or \
    os.stat("%s_001.pdb" %prefix)[6]==0:
    command='phenix.refine %s > %s_afitt.log' %(ref_args, prefix)
    print command
    # try:
    #   subprocess.check_call(command,shell=True)
    # except subprocess.CalledProcessError:
    #   print "ERROR: %s refinement went wrong." %(code)
    #   subprocess.call('echo %s >>../wrong1.txt' %code, shell=True)
    #   status=0
  else:
    print "FINISHED PREVIOUSLY"
    status=1
  os.chdir('..')
  return status



def get_resname_resid(code,target_lig, f, g):
  ligands={}
  resnames=[target_lig]
  #~ for resname in resnames:
  command= 'mmtbx.afitt %s_oe.pdb %s_oe.cif %s' %(code, code, target_lig)
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

def get_energy(pdbfile, code, target_lig, prefix, f, header):
  os.chdir(code)
  f.write("sc_%-7s" %prefix)
  if code != '25c8' and prefix !='elbow':
    command= 'mmtbx.afitt %s ../%s_oe.cif %s' %(pdbfile, code, target_lig)
    print command
    x=subprocess.check_output(command, shell=True)
    x=[line for line in x.split('\n') if line]
    for instance in header:
      for line in x:
        now_instance='%-9s' %line.split()[0]
        if instance == now_instance:
          f.write("%9.4f  " %float(line.split()[2]))
  f.write("\n")
  os.chdir('..')

def get_rfree(logfile, code, target_lig, prefix, f, header):
  os.chdir(code)
  f.write("sc_%-7s" %prefix)
  if code != '25c8' and prefix !='elbow':
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


#======================================================================#

codes = get_codes("filelist.txt")
failed_codes = get_codes("failed.txt")
codes = [code for code in codes if code not in failed_codes]
special_codes={'1p62':'GEO','1hq2':'PH2','1dib':'L34','1c5x':'ESI','1mbi':'IMD',
       '1ukz':'AMQ','1ia1':'TQ3','1yv3':'BIT','1cde':'GAR','1hnn':'SKF',
       '1exa':'394','1hdy':'PYZ','1lrh':'NLA','1frp':'FDP','1sq5':'PAU',
       '1fcx':'184','1fcz':'156','1ive':'ST3','1t40':'ID5','1t9b':'1CS',
       '1meh':'MOA','1coy':'AND','1pbd':'PAB','1mmv':'3AR',
       '1hww':'SWA','1j3j':'CP6','1d3h':'A26'
       }
lig_dict, all_lig_dict = get_code_lig_dict()
for code in failed_codes:
  del lig_dict[code]
  del all_lig_dict[code]
for code in special_codes:
  lig_dict[code] = special_codes[code]

elbow_error_codes=[]
with open('elbow_refine_errors.txt', 'r') as f:
  for line in f.readlines():
    elbow_error_codes.append(line.split()[1])



#INITIAL STUFF ONLY HAD TO RUN ONCE
# import code; code.interact(local=dict(globals(), **locals()))
# make_elbow_cif_from_pdb_repo(all_lig_dict)
# make_elbow_cif_from_input_file(all_lig_dict, elbow_error_codes)


# RANGE FOR EACH PROCESSOR
t_range=[0,46]
# t_range=[46,92]
# t_range=[92,138]
# t_range=[138,194]
t_range=[0,194]

ij=1
prefixes = ['elbow','no_afitt__','sc_10_adp_','sc_10_adp_']
for code in lig_dict.keys()[t_range[0]:t_range[1]]:
  print " \nCOUNT %d " %ij
  target_lig = lig_dict[code]
  other_ligs = [lig for lig in all_lig_dict[code] if lig != target_lig]
  print "\n"+"="*100
  print "code:%s traget_lig:%s other_ligs:%s" %(code, target_lig,
                                  ' '.join(str(p) for p in other_ligs) )
  assert os.path.isfile('%s_%s_elbow.cif' %(code, target_lig)), "%s %s" %(code, target_lig)
  assert os.path.isfile('%s_oe.cif' %(code)), "%s" %(code)

  f=open('%s/%s_energy.dat' %(code,code), 'w')
  g=open('%s/%s_rfree.dat' %(code,code), 'w')
  ligands=get_resname_resid(code,target_lig,f,g)
  header=file_header(ligands)
  get_energy('../%s_oe.pdb' %code, code, target_lig, 'deposi    ', f,header)

  for prefix in prefixes:
    ref_args = "%s_10refined_001.pdb %s_10refined_001.mtz " \
               "../%s_oe.cif ../%s_%s_elbow.cif " \
               "output.prefix=%s_%s " \
               "--overwrite " \
               "refinement.main.number_of_macro_cycles=5 " \
               %(code, code, code, code, target_lig, code, prefix)
    ref_result = refine(code, ref_args, prefix)
    if ref_result:
      get_energy("%s_%s_001.pdb" %(code,prefix), code, target_lig, '%-10s'%prefix, f, header)
      get_rfree("%s_%s_001.log" %(code,prefix),  code, target_lig, '%-10s'%prefix, g, header)


  f.close()
  g.close()
  ij+=1
sys.exit()






# for code in codes:
#    i+=1
#    print "REFINE %d" %i
#    make_dir(code)
#    f=open('%s/%s_energy.dat' %(code,code), 'w')
#    g=open('%s/%s_rfree.dat' %(code,code), 'w')
#    ligands=get_resname_resid(code,f,g)
#    header=file_header(ligands)
#    get_energy('../%s_oe.pdb' %code, code,'deposi    ', 'deposi',ligands, f,header)
#    for ref_args, prefix,scale in ref_args_prefix:
#      ref_result=refine(code, scale, ref_args, prefix)
#      # ref_result=True
#
#    f.close()
#    g.close()
#    print("=============================================================\n")










#
#
# def run_initial_refine(code):
#   os.chdir(code)
#   status=1
#   print "Refining: %s " %(code)
#   # run refinements
#   if not os.path.isfile("%s_10refined_001.pdb" %(code)) or \
#     os.stat("%s_10refined_001.pdb" %(code))[6]==0:
#     command='phenix.refine ../%s_oe.pdb ' \
#             '../%s_start_rfree.mtz ' \
#             '../%s_oe.cif ' \
#             'output.prefix=%s_10refined '  \
#             '--overwrite ' \
#             'refinement.main.number_of_macro_cycles=10 '  \
#             '--quiet' %(code, code, code, code)
#     print command
#     try:
#       subprocess.check_call(command,shell=True)
#     except subprocess.CalledProcessError:
#       print "ERROR: %s refinement went wrong." %(code)
#       subprocess.call('echo %s_initial >>../wrong1.txt' %code, shell=True)
#       status=0
#   os.chdir('..')
#   return status