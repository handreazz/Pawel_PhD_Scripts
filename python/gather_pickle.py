#! /usr/bin/env python

import os, sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set_context("poster")

cwd = os.getcwd()
pdbs = []
with open('success_pdb.txt', 'r') as f:
  for line in f.readlines():
    pdbs.append(line.strip()[0:4])
bad_pdbs = []
with open('amberprep_error_pdb.txt', 'r') as f:
    for line in f.readlines():
      bad_pdbs.append(line.strip().split()[3])
pdbs = [ i for i in pdbs if i not in bad_pdbs]
data=np.zeros((4,13, len(pdbs)))

pdb_counter=0
for i_pdb,pdb in enumerate(pdbs):
  os.chdir('data/%s/%s' %(pdb[1:3], pdb))
  if not os.path.isfile('Summary_%s.dat' %pdb):
    os.chdir(cwd)
    continue
  print "="*100,"\n%s %d" %(pdb, i_pdb)
  with open('Summary_%s.dat' %pdb) as f:
    f.readline()
    line_counter = 0
    for line in f:
      line = line.strip().split()[1:]
      for i, val in enumerate(line):
        data[line_counter, i, pdb_counter] = val
      line_counter += 1
  pdb_counter += 1
  os.chdir(cwd)

rows = '''EH
  0.025
  0.050
  0.075
  '''.split()

cols = '''clash
  hbond
  MolP_sc
  Rama_outl
  Rama_fav
  Rotam
  Cbeta
  RMS_bnd
  RMS_ang
  Reso
  Rwork
  Rfree
  Rdiff
  '''.split()

wp = pd.Panel(data, items=rows, major_axis=cols, minor_axis=pdbs)
wp = wp.transpose(2, 0, 1)
import pickle
PIK = "pickle.dat"
with open(PIK, "wb") as f:
    pickle.dump(wp, f)

# import code ; code.interact(local=dict(globals(), **locals()))
