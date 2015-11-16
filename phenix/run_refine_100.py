#! /usr/bin/env python

import os, sys
import subprocess

proc=0
pdbs_to_run=10

pdbs = []
with open('mtz.txt', 'r') as f:
  for line in f.readlines():
    pdbs.append(line.strip()[0:4])

n = len(pdbs)
i_run = [i for i in range(n) if i%12==proc ]
pdbs_completed=0

for i in i_run:
  if pdbs_completed >= pdbs_to_run: break
  pdb= pdbs[i]
  print "="*100,"\n%s" %pdb
  os.chdir(pdb)

  command_fixed = 'phenix.refine 4phenix_%s_minall.pdb %s.mtz ' \
           '"strategy=*individual_sites individual_sites_real_space rigid_body *individual_adp group_adp tls *occupancies group_anomalous" ' \
           'topology_file_name=4amber_%s.prmtop ' \
           'amber.coordinate_file_name=4amber_%s.rst7 ' \
           'refinement.main.number_of_macro_cycles=10 ' \
           'write_geo=False --overwrite  use_sander=True ' %(pdb, pdb, pdb, pdb)

  #EH
  pfx = 'EH'
  if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
    print "refine %s" %pfx
    command_change = 'refinement.target_weights.optimize_xyz_weight=False ' \
                     'use_amber=False ' \
                     'output.prefix=%s '  \
                     'wxc_scale=0.5 amber.wxc_factor=None ' \
                     'use_c_beta_deviation_restraints=True '\
                     'discard_psi_phi=True ' %pfx
    command = command_fixed + command_change
    out = subprocess.check_output(command,shell=True)
    print '     %s' %([i for i in out.split('\n') if i!=''][-1])
  else:
    print "refine %s: already done" %pfx
    with open('%s_001.log' %pfx) as f:
        print '     %s' %(f.readlines()[-1].strip())

  #EH
  pfx = 'EH_opt'
  if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
    print "refine %s" %pfx
    command_change = 'refinement.target_weights.optimize_xyz_weight=True ' \
                     'use_amber=False ' \
                     'output.prefix=%s '  \
                     'wxc_scale=0.5 amber.wxc_factor=None ' \
                     'use_c_beta_deviation_restraints=True '\
                     'discard_psi_phi=True ' %pfx
    command = command_fixed + command_change
    out = subprocess.check_output(command,shell=True)
    print '     %s' %([i for i in out.split('\n') if i!=''][-1])
  else:
    print "refine %s: already done" %pfx
    with open('%s_001.log' %pfx) as f:
        print '     %s' %(f.readlines()[-1].strip())

  #ratio_opt
  pfx = 'ratio_opt'
  if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
    print "refine %s" %pfx
    command_change = 'refinement.target_weights.optimize_xyz_weight=True ' \
                     'use_amber=True ' \
                     'output.prefix=%s ' \
                     'wxc_scale=0.5 amber.wxc_factor=None ' \
                     'use_c_beta_deviation_restraints=False '\
                     'discard_psi_phi=False '  %pfx
    command = command_fixed + command_change
    out = subprocess.check_output(command,shell=True)
    print '     %s' %([i for i in out.split('\n') if i!=''][-1])
  else:
    print "refine %s: already done" %pfx
    with open('%s_001.log' %pfx) as f:
        print '     %s' %(f.readlines()[-1].strip())

  #noratio_opt
  pfx = 'noratio_opt'
  if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
    print "refine %s" %pfx
    command_change = 'refinement.target_weights.optimize_xyz_weight=True ' \
                     'use_amber=True ' \
                     'output.prefix=%s ' \
                     'wxc_scale=0.5 amber.wxc_factor=0.5 ' \
                     'use_c_beta_deviation_restraints=False '\
                     'discard_psi_phi=False '  %pfx
    command = command_fixed + command_change
    out = subprocess.check_output(command,shell=True)
    print '     %s' %([i for i in out.split('\n') if i!=''][-1])
  else:
    print "refine %s: already done" %pfx
    with open('%s_001.log' %pfx) as f:
        print '     %s' %(f.readlines()[-1].strip())

  #ratio
  for weight in [0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5]:
    pfx = 'ratio_%s' %weight
    if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
      print "refine %s" %pfx
      command_change = 'refinement.target_weights.optimize_xyz_weight=False ' \
                       'use_amber=True ' \
                       'output.prefix=%s ' \
                       'wxc_scale=%s amber.wxc_factor=None ' \
                       'use_c_beta_deviation_restraints=False '\
                       'discard_psi_phi=False '  %(pfx, weight)
      command = command_fixed + command_change
      out = subprocess.check_output(command,shell=True)
      print '     %s' %([i for i in out.split('\n') if i!=''][-1])
    else:
      print "refine %s: already done" %pfx
      with open('%s_001.log' %pfx) as f:
          print '     %s' %(f.readlines()[-1].strip())

  #noratio
  for weight in [0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5]:
    pfx = 'noratio_%s' %weight
    if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
      print "refine %s" %pfx
      command_change = 'refinement.target_weights.optimize_xyz_weight=False ' \
                       'use_amber=True ' \
                       'output.prefix=%s ' \
                       'wxc_scale=0.5 amber.wxc_factor=%s ' \
                       'use_c_beta_deviation_restraints=False '\
                       'discard_psi_phi=False '  %(pfx, weight)
      command = command_fixed + command_change
      out = subprocess.check_output(command,shell=True)
      print '     %s' %([i for i in out.split('\n') if i!=''][-1])
    else:
      print "refine %s: already done" %pfx
      with open('%s_001.log' %pfx) as f:
          f.seek(-2000, 2)
          print '     %s' %(f.readlines()[-1].strip())

  os.chdir('..')
  pdbs_completed+=1







# import code; code.interact(local=dict(globals(), **locals()))