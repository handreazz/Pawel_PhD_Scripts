#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
from Scientific.IO import NetCDF as Net
from Bio.PDB import *


A=prmtop('../4lztSh.prmtop')
masses=A.Get_Masses()

B=rst7('../4lztSh.rst7')
coords=B.Get_Coords()

com=COM(coords,masses)
print com
#~ print coords.shape
#~ print coords[0,:]

print '############################\n\n'

ofile = Net.NetCDFFile('../ptraj/mergtraj_cent.nc','a')
traj=ofile.variables['coordinates']
x=traj[0,:,:]
ofile.close()

com=COM(x,masses)

print com
#~ print x.shape
#~ print x[0,:]

moveby=coords[0,:]-x[0,:]
print moveby
print '############################\n\n'

f=open('ptraj_translate', 'w')
f.write('trajin ../ptraj/mergtraj_cent.nc\n')
f.write('translate x %10.6f y %10.6f.2 z %10.6f \n' %(moveby[0],moveby[1],moveby[2]))
f.write('trajout mergtraj_centonpdb.nc netcdf\n')
f.close()
os.system('ptraj ../4lztSh.prmtop <ptraj_translate')

ofile = Net.NetCDFFile('mergtraj_centonpdb.nc','a')
coords=ofile.variables['coordinates']
x=coords[0:5,:,:]
ofile.close()
for i in range(5):
	com=COM(x[i,:,:],masses)
	print com

print '############################\n\n'



