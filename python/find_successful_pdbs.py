#! /usr/bin/env python

import os,sys
from glob import glob
import argparse

def search_subdirs(dir, pattern):
  '''
  Search for files in directory and subdirectories.
  Arguments
    dir: directory to search
    pattern: unix ls style search pattern
    files: python list where names of files will be appended
  '''
  files=[]
  for file in glob("%s/%s" %(dir,pattern)):
    files.append(file)
  for subdir in os.walk(dir).next()[1]:
    deepfiles = search_subdirs("%s/%s" %(dir,subdir),pattern)
    files = files+deepfiles
  return files

dir = "/net/casegroup2/u2/pjanowsk/Case/4lzt/RunSh"
pattern = "*dat"
files = search_subdirs(dir,pattern)

with open('success_pdb.txt', 'w') as f:
  for file in files:
    code = os.path.basename(file)[0:4])
    cmd = "grep 'CRYST1' %s/%s/%s.pdb | head -n 1" %(code[1:3], code, code)
    sg = subprocess.check_output(cmd, shell=True)[55:].strip()
    cmd = "grep 'Resolution range:' %s/%s/%s_refine_scale_0.050_001.log | head -n 1" %(code[1:3], code, code)
    reso = subprocess.check_output(cmd, shell=True).strip().split()[-1]
    f.write('%s  %20s %3.1f\n' %(code, sg, float(reso)) )






# import code; code.interact(local=dict(globals(), **locals()))