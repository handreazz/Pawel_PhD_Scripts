import os, sys
import matplotlib.pyplot as plt
from numpy import *
import seaborn as sns
import re

sns.set_style("whitegrid")


#======================================================================#
#
#  ENERGY AND RFREE
#
#======================================================================#

with open('filelist.txt') as f:
  codes=[x.strip().split('_')[0] for x in f.readlines()]
with open('failed.txt') as f:
  failed=[x.strip() for x in f.readlines()]
codes = [x for x in codes if x not in failed]

en_10 = []
en_noaf = []
en_depo = []
en_elbo = []
en_10_20 = []
en_depo_10 = []
en_noaf_10 = []
en_elbo_10 = []

rfree_10 = []
rfree_noaf = []
rfree_depo = []
rfree_elbo = []
rfree_noaf_10 = []
rfree_20_noaf = []
rfree_10_20 = []
rfree_elbo_10 = []

for code in codes:
  with open('%s/%s_energy.dat' %(code,code)) as f:
    lines=f.readlines()
  n_lig = len(lines[0].split())
  for line in lines:
    if line[0:13] == 'sc_deposi    ':
      dep_line = line.strip()[13:].split()
    elif line[0:13] ==  'sc_sc_10_adp_':
      sc10_line = line.strip()[13:].split()
    elif line[0:13] ==  'sc_no_afitt__':
      noaf_line = line.strip()[13:].split()
    elif line[0:13] ==  'sc_elbow     ':
      elbow_line = line.strip()[13:].split()

  depo = dep_line[0:n_lig]
  sc10 = sc10_line[0:n_lig]
  noaf = noaf_line[0:n_lig]
  elbo = elbow_line[0:n_lig]


  depo = array([float(x) for x in depo])
  sc10 = array([float(x) for x in sc10])
  noaf = array([float(x) for x in noaf])
  elbo = array([float(x) for x in elbo])

  en_depo_10_c = list((depo - sc10))
  en_noaf_10_c = list((noaf - sc10))
  en_elbo_10_c = list((elbo - sc10))

  en_depo_10_c = list((depo-sc10)/depo*100)
  en_noaf_10_c = list((noaf-sc10)/noaf*100)
  en_elbo_10_c = list((elbo-sc10)/elbo*100)

  for i, z in enumerate(en_elbo_10_c):
    if z >90.:
      print "Code:%s Instance:%d eLBOW:%.2f AFITT:%.2f delta(%%):%.2f " \
            %(code, i, elbo[i], sc10[i], en_elbo_10_c[i])

  en_depo_10 = en_depo_10 + en_depo_10_c
  en_noaf_10 = en_noaf_10 + en_noaf_10_c
  en_elbo_10 = en_elbo_10 + en_elbo_10_c

  en_10 = en_10 + list(sc10)
  en_noaf = en_noaf + list(noaf)
  en_depo = en_depo + list(depo)
  en_elbo = en_elbo + list(elbo)

  sc10, noaf, elbo = None, None, None
  with open('%s/%s_rfree.dat' %(code,code)) as f:
    for line in f.readlines():
      if line[0:13] ==  'sc_sc_10_adp_':
        sc10 = float(line.strip()[13:].split()[1])
      elif line[0:13] ==  'sc_no_afitt__':
        noaf = float(line.strip()[13:].split()[1])
      elif line[0:13] ==  'sc_elbow     ':
        elbo = float(line.strip()[13:].split()[1])

    rfree_noaf_10.append(noaf-sc10)
    rfree_elbo_10.append(elbo-sc10)
    rfree_10.append(sc10)
    rfree_noaf.append(noaf)
    rfree_elbo.append(elbo)


print "mean afitt E: %f" %mean(en_10)
print "mean EH E:    %f" %mean(en_noaf)
print "mean PDB E:   %f" %mean(en_depo)
print "mean eLBOW E:   %f" %mean(en_elbo)
print "mean afitt Rfree: %f" %mean(rfree_10)
print "mean EH Rfree:    %f" %mean(rfree_noaf)
print "mean eLBOW Rfree:    %f" %mean(rfree_elbo)
print "Total ligands: %d" %len(en_10)


#======================================================================#
#
#  TIMING
#
#======================================================================#


EH_times={}
AF_times={}
with open('timings_EH.txt') as f:
  for line in f:
    code=line[0:4]
    time=float(line.split()[-2])
    EH_times[code]=time

with open('timings_AFITT.txt') as f:
  for line in f:
    code=line[0:4]
    time=float(line.split()[-2])
    AF_times[code]=time

with open('failed.txt') as f:
  failed=[x.strip() for x in f.readlines()]

codes=AF_times.keys()
codes = [code for code in codes if code not in failed]
n_codes = len(codes)


rows_to_delete=[]
data=zeros((n_codes,2))
for i,code in enumerate(codes):
  perc=(EH_times[code] - AF_times[code]) /EH_times[code]*100
  if perc <-100:
    print "%s EHtime:%.0f AFtime:%.0f Percent:%.2f " %(code, EH_times[code], AF_times[code], perc)
    rows_to_delete.append(i)

  else:
    data[i,0] = EH_times[code]
    data[i,1] = AF_times[code]

for row in reversed(rows_to_delete):
  data = delete(data,(row), axis=0)

times_noaf=data[:,0]
times_10=data[:,1]
times_noaf_10 = (times_noaf-times_10)/times_noaf*100


#======================================================================#
#
#  MOGUL
#
#======================================================================#
# bonds
mogul_bond_depo = []
mogul_bond_noaf = []
mogul_bond_10   = []
with open('/home/pjanowsk/c/OpenEye/afitt/mogul/all/BOND.dat', 'r') as f:
  appendto = None
  for line in f:
    if line.startswith('@'):
      appendto = None
    if line.startswith('&'):
      continue
    if 'G1.S0' in line:
      appendto = 'pdb'
    elif 'G1.S1' in line:
      appendto = 'afitt-cif'
    elif 'G1.S2' in line:
      appendto = 'phenix-afitt'
    elif appendto == 'pdb':
      mogul_bond_depo.append([float(i) for i in line.split()])
    elif appendto == 'afitt-cif':
      mogul_bond_noaf.append([float(i) for i in line.split()])
    elif appendto == 'phenix-afitt':
      mogul_bond_10.append([float(i) for i in line.split()])
mogul_bond_depo = array(mogul_bond_depo)
mogul_bond_noaf = array(mogul_bond_noaf)
mogul_bond_10   = array(mogul_bond_10)

# angles
mogul_ang_depo = []
mogul_ang_noaf = []
mogul_ang_10   = []
with open('/home/pjanowsk/c/OpenEye/afitt/mogul/all/ANGLE.dat', 'r') as f:
  appendto = None
  for line in f:
    if line.startswith('@'):
      appendto = None
    if line.startswith('&'):
      continue
    if 'G1.S0' in line:
      appendto = 'pdb'
    elif 'G1.S1' in line:
      appendto = 'afitt-cif'
    elif 'G1.S2' in line:
      appendto = 'phenix-afitt'
    elif appendto == 'pdb':
      mogul_ang_depo.append([float(i) for i in line.split()])
    elif appendto == 'afitt-cif':
      mogul_ang_noaf.append([float(i) for i in line.split()])
    elif appendto == 'phenix-afitt':
      mogul_ang_10.append([float(i) for i in line.split()])
mogul_ang_depo = array(mogul_ang_depo)
mogul_ang_noaf = array(mogul_ang_noaf)
mogul_ang_10   = array(mogul_ang_10)


import pickle
PIK = "pickle.dat"
data_for_pickle = [en_10, en_noaf, en_depo, en_elbo, en_10_20, en_depo_10,
                   en_noaf_10, en_elbo_10, rfree_10, rfree_noaf,
                   rfree_depo, rfree_elbo, rfree_noaf_10, rfree_20_noaf,
                   rfree_10_20, rfree_elbo_10, times_noaf, times_10, times_noaf_10,
                   mogul_bond_depo, mogul_bond_noaf, mogul_bond_10,
                   mogul_ang_depo, mogul_ang_noaf, mogul_ang_10]
with open(PIK, "wb") as f:
    pickle.dump(data_for_pickle, f)


