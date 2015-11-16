#! /usr/bin/env python

# Pawel Janowski, David Case Group, Rutgers U., Jan. 2015

#=====================================================================#
# Calculate TLS parameters given a PDB file with Uij or B-factors.    #
#                                                                     #
# Arguments:                                                          #
#     -i input pdb file (if ANISOU present will use that, otherwise   #
#        uses B-factors)                                              #
#     -o prefix of output files. Prints $prefix.pdb and $prefix.dat   #
# Example usage:                                                      #
#     adp2tls.py -i 4lzt.pdb -o tls1                                  #
#######################################################################

import sys, os
import numpy as np
import argparse


def run(infile, prefix):
  print infile
  print prefix


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--infile", help="input PDB file (min 4 atoms).")
  parser.add_argument("-o", "--prefix", help="prefix for output .pdb and .dat files", default="out")
  args = parser.parse_args()
  print args
  #check existence of input file

  run(args.infile, args.prefix)

