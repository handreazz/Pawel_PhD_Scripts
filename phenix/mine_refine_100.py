#! /usr/bin/env python

import os, sys
import subprocess

pdbs = []
with open('mtz.txt', 'r') as f:
  for line in f.readlines():
    pdbs.append(line.strip()[0:4])

pdbs=['424d']
for i_pdb,pdb in enumerate(pdbs):  
  print "="*100,"\n%s %d" %(pdb, i_pdb)
  os.chdir(pdb)

  if os.path.isfile('Summary_%s.dat' %pdb):
    with open('Summary_%s.dat' %pdb) as f:
      if len(f.readlines()) == 21:
        print "  Already done."
        os.chdir('..')
        continue

  fsummary = open('Summary_%s.dat' %pdb, 'w')
  fsummary.write("               Rfree    clash  hbond  MolP_sc  "
                     "Rama_outl  Rama_fav  Rotam  Cbeta  RMS_bnd  "
                     "RMS_ang  Reso   Rwork\n")
  pfxs = '''EH
    EH_opt
    noratio_opt
    ratio_opt
    ratio_0.006
    ratio_0.01
    ratio_0.02
    ratio_0.04
    ratio_0.08
    ratio_0.15
    ratio_0.3
    ratio_0.5
    noratio_0.006
    noratio_0.01
    noratio_0.02
    noratio_0.04
    noratio_0.05
    noratio_0.08
    noratio_0.15
    noratio_0.3
    noratio_0.5
    '''

  for pfx in pfxs.split():
    if not os.path.isfile("%s_001.pdb" %pfx) or os.stat("%s_001.pdb" %pfx)[6]==0:
      print "  %s MISSING" %pfx
    else:
      print "  %s " %pfx
      command = 'phenix.molprobity %s_001.pdb | grep "= Summary =" -A 13' \
                ' >molprob_%s.txt' %(pfx, pfx)
      subprocess.call(command,shell=True)

      with open('ctraj.hbond.in', 'w') as f:
        f.write('parm asu.prmtop\n')
        f.write('trajin %s_001.pdb\n' %pfx)
        f.write('hbond out tmp.dat dist 3.5\n')
        f.write('go\n')
      subprocess.call('cpptraj -i ctraj.hbond.in > /dev/null', shell=True)
      command = 'awk \'FNR == 2 {print "  H_bonds               = "$2}\'' \
                ' tmp.dat >>molprob_%s.txt' %pfx
      subprocess.call(command,shell=True)

      results = {}
      with open('molprob_%s.txt' %pfx) as f:
        lines=f.readlines()
        lines=[line.split() for line in lines if line.split()]
        #~ import code; code.interact(local=dict(globals(), **locals()))
        for line in lines:
          if line[0] == 'Ramachandran':
            results['ramaout'] = float(line[3])
          if line[0] == 'favored':
            results['ramafav'] = float(line[2])
          if line[0] == 'Rotamer':
            results['rotam'] = float(line[3])
          if line[0] == 'C-beta':
            results['cbeta'] = float(line[3])
          if line[0] == 'Clashscore':
            results['clash'] = float(line[2])
          if line[0] == 'RMS(bonds)':
            results['rmsbonds'] = float(line[2])
          if line[0] == 'RMS(angles)':
            results['rmsangle'] = float(line[2])
          if line[0] == 'MolProbity':
            results['molprob'] = float(line[3])
          if line[0] == 'Resolution':
            results['resol'] = float(line[2])
          if line[0] == 'R-work':
            results['rwork'] = float(line[2])
          if line[0] == 'R-free':
            results['rfree'] = float(line[2])
          if line[0] == 'H_bonds':
            results['hbonds'] = float(line[2])

      fsummary.write("%-13s  " %pfx)
      def fsummary_write (frmt, prop):
        if prop in results.keys():
          fsummary.write(frmt %results[prop])
        else:
          fsummary.write(frmt %0)  
      
      fsummary_write("%6.4f  ", 'rfree')
      fsummary_write("%6.2f  ", 'clash')
      fsummary_write("%4d  "  , 'hbonds')
      fsummary_write("%6.2f    ", 'molprob')
      fsummary_write("%6.2f      ", 'ramaout')
      fsummary_write("%6.2f   ", 'ramafav')
      fsummary_write("%5.2f  ", 'rotam')
      fsummary_write("%3d     ", 'cbeta')
      fsummary_write("%6.4f  ", 'rmsbonds')
      fsummary_write("%6.2f ", 'rmsangle')
      fsummary_write("%6.2f   ", 'resol')
      fsummary_write("%6.4f", 'rwork')
      fsummary.write("\n")

  fsummary.close()
  os.chdir('..')




