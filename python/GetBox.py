#! /usr/bin/python
import ReadAmberFiles as raf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("pdbfile", help="name of pdb file")
args = parser.parse_args()
pdb=raf.pdb(args.pdbfile)
box=pdb.Get_Box()
print( " %7.3f %7.3f %7.3f %7.3f %7.3f %7.3f " %(box[0],box[1],box[2],box[3],box[4],box[5]) )
