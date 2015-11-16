#!/usr/bin/env python
import os
from numpy import *
from Scientific.IO import NetCDF
from ReadAmberFiles import *
import argparse


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
    f.write("%10.8f   %10.8f   %10.8f\n" %(com[0], com[1], com[2]))
  f.close()
  return array(coms)


#~ nc_name='/net/cottus/u2/cliu/try/new/fit.nc'
nc_name='fit.nc'
#~ topo_name='/net/cottus/u2/cliu/try/new/supercell.parm7'
topo_name='sc_noH.prmtop'
out_name='tmp.dat'
#~ exp_rst7='/net/cottus/u2/cliu/try/new/nowat.Xtal22xbox.crd'
exp_rst7='sc_noH.rst7'

comarray=get_traj_com(nc_name, topo_name, out_name)
#~ comarray=genfromtxt('tmp.dat')
a=rst7(exp_rst7)
c=a.Get_Coords()
topo=prmtop(topo_name)
masses=topo.Get_Masses()
com=COM(c, masses)
#~ print com
#~ print comarray[1,:]
#~ import code; code.interact(local=locals())

comarray=comarray-com
savetxt('tmp1.dat', comarray,fmt='%8.6f')

import matplotlib.pyplot as plt
fig=plt.figure(figsize=(30, 10))
ax = fig.add_subplot(1,3,1)
ax.scatter(comarray[:,0], comarray[:,1])
plt.xlabel('x')
plt.ylabel('y',labelpad=0)


ax = fig.add_subplot(1,3,2)
ax.scatter(comarray[:,0], comarray[:,2])
plt.xlabel('x')
plt.ylabel('z',labelpad=0)
plt.title('comarray')

ax = fig.add_subplot(1,3,3)
ax.scatter(comarray[:,1], comarray[:,2])
plt.xlabel('y')
plt.ylabel('z',labelpad=0)

for ax in fig.axes:
  ax.set_xlim(-0.002,0.002)
  ax.set_ylim(-0.002,0.002)

plt.savefig('sc2_com.png')
