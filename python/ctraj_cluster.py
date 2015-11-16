#! /usr/bin/python
import sys
import os
from numpy import *


residues=[":8-17,25-35", ":25-35,42-52", ":3-56"]
atoms=["@CA", "@N,C,O"]
fit=["rms_fitboth", "rms_fitone", "rms_nofit"] 
fit=["rms_fitone"] 
skipframes=10
sieve=10

for r in residues:
  if r[1]=='8': r_label='h12'
  elif r[1]=='3':r_label='all'
  else: r_label='h23'
  for a in atoms:
    a_label=a[1:]
    for fi in fit:
      fi_label=fi

      f=open('ctraj_cluster','w')
      f.write("parm ../asu.prmtop\n")
      for i in range(27):
          for j in range(2):
            f.write("trajin ../revsym/RevSym_%02d_%02d.nc 1 -1 %d\n" %((i+1),(j+1),skipframes))

      if fi=="rms_fitboth":
        f.write("cluster rms mass %s%s clusters 10 sieve %d " %(r,a, sieve))        
      elif fi=="rms_fitone":
        print "rms_fitone"
        f.write("reference ../asu.rst7\n")
        f.write("rmsd reference :25-35@N,C\n")
        #~ f.write("go\n")
        f.write("cluster rms mass nofit %s%s clusters 10 sieve %d " %(r,a, sieve))        
      elif fi=="rms_nofit":
        f.write("cluster rms mass nofit %s%s clusters 10 sieve %d " %(r,a, sieve))      
      
      f.write("summary %s_%s_%s.summary.dat " %(r_label, fi_label, a_label) )
      f.write("info %s_%s_%s.info.dat " %(r_label, fi_label, a_label) )
      f.write("out %s_%s_%s.cnumvtime.dat " %(r_label, fi_label, a_label) )
      f.write("repout %s_%s_%s.2 repfmt restart \n" %(r_label, fi_label, a_label) ) 
      f.close()
      os.system("cpptraj -i ctraj_cluster")
      
