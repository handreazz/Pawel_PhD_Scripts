#!/usr/bin/env python
import os, sys
from numpy import *

# A jiffy script to analyze stuff in the .dat files. Columns 3-21 (adps,
# etc.) are read into "d". Residue number and atom name are read into 'r'
# Then you can filter selection (eg. backbone atoms, residues, less than a
# specific b-factor difference, etc). Then corr prints correlations between
# each adp, bfactor, and anisotropy.

filename=sys.argv[1]

f=open(filename, 'r')
x=[]
for i in f.readlines():
    x.append(i.strip().split() )
x=x[1:]    
x=array(x)

r=x[:,0:2]
d=float32(x[:,2:])
d_names = x[:,0:2]

i=bool_(ones(1001))

def corr(d):
	for i in range(7):
		print ("%4.3f " %(corrcoef(d[:,i], d[:,i+7])[0,1]) ),
	print ("%4.3f " %(corrcoef(d[:,17], d[:,18])[0,1]))

# Filter for B-factor/anisotropy difference
print d.shape
data1=abs(d[:,6]-d[:,13])
data2=abs(d[:,17]-d[:,18])
index=(data1<10) & (data2<3)
print sum(index)
d=d[index]
d_names= d_names[index]

corr(d)

#corrcoef of all adps
exp=list(d[:,0])+list(d[:,1])+list(d[:,2])+list(d[:,3])+list(d[:,4])+list(d[:,5])
sim=list(d[:,7])+list(d[:,8])+list(d[:,9])+list(d[:,10])+list(d[:,11])+list(d[:,12])
print corrcoef(exp,sim)

import iotbx.pdb
from scitbx.array_family import flex
from cctbx import adptbx

def get_hieratchy(file_name):
  pdb_inp = iotbx.pdb.input(file_name=file_name) 
  h = pdb_inp.construct_hierarchy()
  return h

def is_good(a):
  get_class = iotbx.pdb.common_residue_names_get_class
  result = False
  resname = a.parent().parent().unique_resnames()[0].strip().upper()
  cl = get_class(name=resname)
  if(cl == "common_amino_acid" or cl == "common_rna_dna"):
    result = True
  if resname in ['HIP', 'HIE', 'HID', 'CYX']:
    return True  
  return result
  


p1 = '4lzt_phenix_refined.pdb'
h1 = get_hieratchy(file_name=p1)
cntr = 0
for a1 in h1.atoms():
  if(is_good(a=a1)):
    done=False
    for a2_i, a2 in enumerate(d_names):
      if (a1.name.strip() == a2[1].strip() and 
              a1.parent().parent().resseq.strip() == a2[0].strip() and
              a1.parent().altloc in ['A','']):
            cntr += 1

            b = d[a2_i][13]
            b = b.astype(float64)
            uij = (d[a2_i][7], d[a2_i][8], d[a2_i][9], 
                   d[a2_i][10], d[a2_i][11], d[a2_i][12])
            uij = array(uij).astype(float64)/10000       
            a1.set_b(b)
            #~ import code; code.interact(local=dict(globals(), **locals()))
            a1.set_uij(uij)
            done=True
            break
    #~ if done==False:
      #~ print a1.name, a1.parent().parent().resseq, a1.parent().altloc
print cntr
h1.write_pdb_file(file_name="my_newADP.pdb")
#~ print d_names[0:10,:]






