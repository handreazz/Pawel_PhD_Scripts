#!/usr/bin/env python
import os
from numpy import *
from Scientific.IO import NetCDF
from ReadAmberFiles import *
import argparse



#checkcom.py - creates the following files. Make sure to set variables
	#exp_com_sc.dat - experimental center of mass of each asu in supercell
	#revsym_com_shifts.dat - average center of mass of each revsym trajectory relative to experimental
	#split_com_shifts.dat - average center of mass of each splittraj trajectory relative to experimental
	#com_revsym_[N]_[M].dat   - center of mass of each frame of each revsym directory
	#com_splittraj_[N]_[M].dat   - center of mass of each frame of each splittraj trajectory


#======================================================================#
# SET VARIABLES
asu_rst7='/u2/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/asu.rst7'
asu_prmtop='/u2/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/asu.prmtop'
asu_pdb='/u2/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/asu.pdb'
ix=3
iy=2
iz=2
revsym_dir='/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/revsym/'
splittraj_dir='/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/splittrajectories/'
#
#======================================================================#


def get_n_asus(pdbfile_name):
  pdbfile=pdb(pdbfile_name)
  smtry,tr =pdbfile.Get_SMTRY()
  return len(smtry)

def ncframes(traj_name):  
  traj = Net.NetCDFFile(traj_name, 'r')
  allcoords=traj.variables['coordinates']
  return allcoords.shape[0]  

def get_exp_com_asu(
    rst7_name,
    topo_name):
  topo=prmtop(topo_name)
  masses=topo.Get_Masses()
  crd=rst7(rst7_name)
  coords=crd.Get_Coords()
  com=COM(coords,masses)
  return com

def get_exp_com_sc(
    rst7_name,
    topo_name,
    pdb_name,
    ix, iy, iz):
    
  exp_com=get_exp_com_asu(asu_rst7, asu_prmtop)
  pdbfile=pdb(pdb_name)
  smtry,tr =pdbfile.Get_SMTRY()
  asymunits=len(smtry)
  UCbox=pdbfile.Get_Box()
  u,invu=CompXfrm(UCbox)
  xv=invu[:,0]
  yv=invu[:,1]
  zv=invu[:,2]
  
  f=open('exp_com_sc.dat','w')
  f.write('%10s   %10s   %10s   %3s   %3s   \n' %('X','Y','Z', 'UC', 'ASU'))
  coms=[]
  for x in range(ix):
    for y in range(iy):
      for z in range(iz):
        uc= z+ 1 + y*iz +x*iz*iy
        #calculate the move vector that was applied
        xmove=(x*(xv[0])+y*(yv[0])+z*(zv[0]))
        ymove=(x*(xv[1])+y*(yv[1])+z*(zv[1]))
        zmove=(x*(xv[2])+y*(yv[2])+z*(zv[2]))
        MoveVector=array([xmove,ymove,zmove],dtype=float32)

        for j in range(asymunits):			
          #get symmetry operations for this asym unit
          s=float32(transpose(smtry[j]))
          t=float32(tr[j])                
          new_com=dot( exp_com, s  ) + t
          new_com=new_com+MoveVector
          coms.append(new_com)
          f.write ("%10.4f   %10.4f   %10.4f   %3d   %3d\n" %(new_com[0], new_com[1], new_com[2], uc, j+1 ))
  f.close()			
  return array(coms)

def get_traj_com(
    nc_name,
    topo_name,
    out_name):
  coms=[]
  nc = NetCDF.NetCDFFile(nc_name, 'r')
  topo=prmtop(topo_name)
  masses=topo.Get_Masses()
  coords=nc.variables['coordinates']  
  f=open(out_name,'w')
  for frame in range(coords.shape[0]):
    this_coords=coords[frame,:,:]
    com=COM(this_coords, masses)
    coms.append(com)
    f.write("%10.4f   %10.4f   %10.4f\n" %(com[0], com[1], com[2]))
  f.close()
  return array(coms)
  
def get_all_com(
    revsym_dir,
    splittraj_dir,
    asu_prmtop_name,   
    n_uc,
    n_asu,
    n_frames):
  
  split_com_array=zeros((n_uc*n_asu,n_frames,3))
  revsym_com_array=zeros((n_uc*n_asu,n_frames,3))
  i=0    
  for uc in range(n_uc):
    for asu in range(n_asu):
      
      print uc, asu
      infile='%s/%02d_%02d.nc' %(splittraj_dir,uc+1, asu+1)
      outfile='com_splittraj_%02d_%02d.dat' %(uc+1, asu+1)
      print infile
      print outfile
      print '\n\n'
      split_com_array[i,:,:]=get_traj_com(infile, asu_prmtop, outfile) 
      
      infile='%s/RevSym_%02d_%02d.nc' %(revsym_dir,uc+1, asu+1)
      outfile='com_revsym_%02d_%02d.dat' %(uc+1, asu+1)
      print infile
      print outfile
      print '\n\n'  
      revsym_com_array[i,:,:]=get_traj_com(infile, asu_prmtop_name, outfile)
      i+=1
  return split_com_array, revsym_com_array
      
def analyze_revsym_avg_coms(
    exp_com,
    revsym_com_array):
  avg_coms=average(revsym_com_array, axis=1)    
  avg_coms=avg_coms-exp_com
  savetxt('revsym_com_shifts.dat',avg_coms,fmt='%10.4f')

def analyze_split_avg_coms(
    exp_coms,
    split_com_array):
  avg_coms=average(split_com_array, axis=1)
  print avg_coms
  for i in range(exp_coms.shape[0]):
    avg_coms[i,:]=avg_coms[i,:]-exp_coms[i,:]
  savetxt('split_com_shifts.dat',avg_coms,fmt='%10.4f')  

    
    


n_uc=ix*iy*iz
n_asu=get_n_asus(asu_pdb)
n_frames=ncframes(splittraj_dir+'/01_01.nc')

exp_coms_sc=get_exp_com_sc(asu_rst7, asu_prmtop, asu_pdb, ix,iy,iz)
split_com_array, revsym_com_array=get_all_com(revsym_dir, splittraj_dir, asu_prmtop, n_uc, n_asu, n_frames)
analyze_revsym_avg_coms(exp_coms_sc[0], revsym_com_array)
analyze_split_avg_coms(exp_coms_sc, split_com_array)




