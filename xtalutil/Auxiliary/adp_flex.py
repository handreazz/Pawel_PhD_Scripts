#! /usr/bin/env phenix.python
import os
import numpy as np
from Scientific.IO import NetCDF
import argparse
from scitbx.array_family import flex
import copy

#######################################################################	
# Calculate ADP's and B-factors from an MD trajectory.                #
#                                                                     #
# Arguments:                                                          #
#     names of netcdf format MD trajectories                          #
#     -s: skip this interval of frames when reading trajectories      #
#         (default=1)                                                 #
#     -ipdb: if set will replace/create B-factor and ANISOU entries   #
#            this pdb file with the newly calculated values           #
#            (No error checking: make sure atom order in provided pdb #
#             and MD trajectories match.)                             #
#     -opdb: name of output pdb file (default="out.pdb"      		  #
# Example usage:                                                      #
#     adp.py md1.nc md2.nc md3.nc -s 10 -ipdb UC.pdb -opdb UC_B.pdb   #
#######################################################################


#get coords array
def get_coords(file, skip_frames):
  ofile = NetCDF.NetCDFFile(file, 'a')
  coords=ofile.variables['coordinates'][::skip_frames,:,:]
  return coords



#print adps to pdb
def print_adp(B, u11, u22, u33, u12, u13, u23, ipdb, opdb):
  ofile=open(opdb,'w')
  cnt=0
  with open(ipdb) as f:
    for line in f:
      line=line.strip()
      if line[0:6] == 'ATOM  ' or line[0:6] == 'HETATM':
        ofile.write('%s%6.2f%-18s\n' %(line[0:60], B[cnt],line[66:]))
        ofile.write('ANISOU%s%7.0f%7.0f%7.0f%7.0f%7.0f%7.0f%-11s\n' %(line[6:28],
                   u11[cnt], u22[cnt], u33[cnt], u12[cnt], u13[cnt], 
                   u23[cnt], line[70:]))
        cnt+=1
      else:
        ofile.write("%-80s\n" %line)
  f.close()

#main run
def run(files, skip_frames, ipdb, opdb):
  coords=0
  for file in files:
    try:
      if coords==0: coords=get_coords(file, skip_frames)
    except:
      coords=np.vstack(( coords,get_coords(file, skip_frames)))

  #V1: use get_adp(coords)
  #~ from phenix.utilities.aniso_from_coords import get_adp
  #~ B, u11, u22, u33, u12, u13, u23 = [], [], [], [], [], [], []
  #~ for atom in range(coords.shape[1]):
    #~ atom_coords=coords[:,atom,:]
    #~ atom_coords=flex.vec3_double(atom_coords.tolist())
    #~ Ba, u11a, u22a, u33a, u12a, u13a, u23a=get_adp(atom_coords,times_10000=True)
    #~ B.append(Ba)
    #~ u11.append(u11a)
    #~ u22.append(u22a)
    #~ u33.append(u33a)
    #~ u12.append(u12a)
    #~ u13.append(u13a)
    #~ u23.append(u23a)

  #V2: use accumulate_aniso()
  from phenix.utilities.aniso_from_coords import accumulate_aniso
  B, u11, u22, u33, u12, u13, u23 = [], [], [], [], [], [], []
  aa=accumulate_aniso()
  for frame in range(coords.shape[0]):
    frame_coords=coords[frame,:,:]
    frame_coords=flex.vec3_double(frame_coords.tolist())
    aa.accumulate(frame_coords)
  aa.calculate_aniso()
  B=aa.b_list.as_numpy_array()
  u11=aa.u11_list.as_numpy_array()*10000
  u22=aa.u22_list.as_numpy_array()*10000
  u33=aa.u33_list.as_numpy_array()*10000
  u12=aa.u12_list.as_numpy_array()*10000
  u13=aa.u13_list.as_numpy_array()*10000
  u23=aa.u23_list.as_numpy_array()*10000

  if (ipdb):
    print_adp(B, u11, u22, u33, u12, u13, u23, ipdb, opdb)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("files",nargs='*', help="names of netcdf trajectory files to get coords")
  parser.add_argument("-s", "--skip_frames", help="trajectory frame skip step (for big datasets)", default=1)
  parser.add_argument("-ipdb", help="if set, will fill the B-factor and ANISOU \
        records of the provided pdb with the calculated values. The pdb \
        must have same number of atoms as the trajectory.")
  parser.add_argument("-opdb", help="output pdb file name", default="out.pdb")
  args = parser.parse_args()
  run(args.files, int(args.skip_frames), args.ipdb, args.opdb)





