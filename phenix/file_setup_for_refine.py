#! /usr/bin/env python

import os, sys
import subprocess

pdbs = []
mtzs = []
with open('mtz.txt', 'r') as f:
  for line in f.readlines():
    pdbs.append(line.strip()[0:4])
    mtzs.append(line.strip())

# print '='*100, "\nGETTING MTZ\n", '='*100
# for pdb, mtz in zip(pdbs, mtzs):
#   print pdb, mtz
#   if not os.path.exists(pdb):
#     os.makedirs(pdb)
#   if os.path.isfile('%s/%s.mtz' %(pdb,pdb)):
#     print "%s.mtz already here" %pdb
#     continue
#   if 'refine_data' in mtz:
#     cci_mtz = '/net/chevy/raid1/nigel/amber/redq/%s/%s/%s'\
#              %(pdb[1:3], pdb, mtz)
#   else:
#     cci_mtz = '/net/cci/share/pdbmtz/mtz_files/%s' %mtz
#   cmd = 'rsync -azvu pawelrc@cci.lbl.gov:%s %s/%s.mtz' %(cci_mtz, pdb, pdb)
#   print cmd
#   subprocess.check_output(cmd, shell=True)
#
# print '='*100, "\nGETTING PDB\n", '='*100
# for pdb in pdbs:
#   print pdb
#   if os.path.isfile('%s/%s.pdb' %(pdb,pdb)):
#     print "%s.pdb already here" %pdb
#     continue
#   cmd = 'phenix.fetch_pdb %s' %pdb
#   print cmd
#   subprocess.check_output(cmd, shell=True)
#   os.rename("%s.pdb" %pdb, "%s/%s.pdb" %(pdb,pdb))
#
# print '='*100, "\nRUNNING AMBERPREP\n", '='*100
# for pdb in pdbs:
#   os.chdir('%s' %pdb)
#   if os.path.isfile('4phenix_%s_minall.pdb' %pdb):
#     print "4phenix_%s_minall.pdb already here" %pdb
#     os.chdir('..')
#     continue
#   cmd = 'phenix.AmberPrep %s.pdb minimise=amber_all clean=on &>amberprep.log' %pdb
#   print cmd
#   subprocess.check_output(cmd, shell=True)
#   os.chdir('..')


#this was without clean and without minimize to get the asu.prmtop necessary for hbonds in cptraj
print '='*100, "\nRUNNING AMBERPREP\n", '='*100
for pdb in pdbs:
  os.chdir('%s' %pdb)
  if os.path.isfile('asu.prmtop'):
    print "4phenix_%s_minall.pdb already here" %pdb
    os.chdir('..')
    continue
  cmd = 'phenix.AmberPrep %s.pdb &>amberprep.log' %pdb
  print cmd
  subprocess.check_output(cmd, shell=True)
  os.chdir('..')