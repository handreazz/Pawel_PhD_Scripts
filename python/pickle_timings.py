#! /usr/bin/env python

import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("poster")

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

t_eh, t_amber, t_ratio, atms = [],[],[],[]
for pdb in pdbs:
  pdb_dir = 'data/%s/%s' %(pdb[1:3], pdb)
  with open("%s/%s_refine_001.log" %(pdb_dir, pdb)) as f:
    f.seek(-250,2)
    for line in f.readlines():
      if "wall clock time" in line:
        t = line.split()[-2]
        t1 = float(t)
  with open("%s/%s_refine_004.log" %(pdb_dir, pdb)) as f:
    f.seek(-250,2)
    for line in f.readlines():
      if "wall clock time" in line:
        t = line.split()[-2]
        t2 = float(t)
  with open("%s/asu.rst7" %pdb_dir) as f:
    f.readline()
    atm = float(f.readline().strip())

  t_eh.append(t1)
  t_amber.append(t2)
  t_ratio.append( t2/t1*100)
  atms.append(atm)

df = np.array( [t_eh, t_amber, t_ratio, atms] ).T
df = pd.DataFrame(df, index=pdbs, columns=['EH', 'amber', 'ratio', 'atoms'])
import pickle
PIK = "pickle_timings.dat"
with open(PIK, "wb") as f:
    pickle.dump(df, f)


# print "\nMean cpu time Amber/EH: %5.2f" %np.mean(df['ratio'])
# print "Correl(d_time, n_atoms): %5.2f\n" %np.corrcoef(df['ratio'], df['atoms'])[0,1]
# x=df['atoms']
# y=df['ratio']
# plt.scatter(x,y)
# plt.xlabel("No. atoms", fontsize=30)
# plt.ylabel("cpu time (% of EH)", fontsize=30)
# plt.tick_params(axis='both', which='major', labelsize=20)
# plt.show()
# # plt.savefig("time_v_natoms.png")
# plt.close()

