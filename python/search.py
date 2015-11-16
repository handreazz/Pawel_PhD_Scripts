#! /usr/bin/env python

import os,sys
from glob import glob
import argparse

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                                                                      #
# This is python library for search routines                           #
#                                                                      #
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def search_subdirs(dir, pattern, files):
  '''
  Search for files in directory and subdirectories.
  Arguments
    dir: directory to search
    pattern: unix ls style search pattern
    files: python list where names of files will be appended
  '''
  for file in glob("%s/%s" %(dir,pattern)):
    files.append(file)
  for subdir in os.walk(dir).next()[1]:
    search_subdirs("%s/%s" %(dir,subdir),pattern, files)


def search(dir, pattern, files):
  '''
  Search for files in directory.
  Arguments
    dir: directory to search
    pattern: unix ls style search pattern
    files: python list where names of files will be appended
  '''
  for file in glob("%s/%s" %(dir,pattern)):
    files.append(file)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-dir", help="directory")
  parser.add_argument("-f", help="file to find")
  args = parser.parse_args()

  files = []
  search_subdirs(args.dir, args.f, files)
  for file in files:
    print file

# import code; code.interact(local=dict(globals(), **locals()))