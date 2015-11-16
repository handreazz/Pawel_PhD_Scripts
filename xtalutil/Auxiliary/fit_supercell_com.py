#!/usr/bin/env python
import os
from numpy import *
from Scientific.IO import NetCDF
from ReadAmberFiles import *
import argparse


#======================================================================#
#                                                                      #
# Fit supercell frames to experimental supercell                       #
#                                                                      #
#======================================================================#


def GetExpCOM(ref_name,topo_name):
  a=rst7(ref_name)
  c=a.Get_Coords()
  topo=prmtop(topo_name)
  h_mask=topo.H_Mask()
  masses=topo.Get_Masses()
  com=COM(c[h_mask], masses[h_mask])
  return com
  
def ShiftFramesByCOM(nc_name, topo_name,exp_com, out_name):
  os.system('cp %s %s' %(nc_name, out_name))
  nc = NetCDF.NetCDFFile(out_name, 'a')
  topo=prmtop(topo_name)
  h_mask=topo.H_Mask()
  masses=topo.Get_Masses()
  coords=nc.variables['coordinates']  
  for frame in range(coords.shape[0]):
    com=COM(coords[frame,:,:][h_mask], masses[h_mask])
    MoveVector=(exp_com-com).astype(float32)
    coords[frame,:,:]=coords[frame,:,:]+MoveVector
  nc.close()
    
if (__name__ == "__main__") :
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--nc_name", help="Trajectory netcdf to fit")
  parser.add_argument("-r", "--ref_name", help="Experimental supercell restart file")
  parser.add_argument("-t", "--topo_name", help="Topology file for supercell")
  parser.add_argument("-o", "--out_name", help="Name of output netcdf file")
  args = parser.parse_args()
  
  exp_com=GetExpCOM(args.ref_name, args.topo_name)
  ShiftFramesByCOM(args.nc_name, args.topo_name, exp_com, args.out_name)
