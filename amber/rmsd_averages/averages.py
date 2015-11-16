#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *

# SET ARGUMENTS
unitcells=1
asymunits=2
topo='../UC.prmtop'
pdb='../UC_centonpdb.rst7'
supercell_trajectory='../mergetraj_centonpdb_nowat.nc'

########################################################################

# Get Frames
traj=nc(supercell_trajectory)
frames=traj.Get_Frames()

# set averages to calculate
dict={5:[frames-500,frames],10:[frames-1000,frames],20:[frames-2000,frames],25:[frames-2500,frames],100:[frames-10000,frames],'all':[1,frames]}



for key in dict:
	#calculate start and end frames
	start=dict[key][0]
	end=dict[key][1]

	#create ptraj averages script and calculate average structures
	f=open('ptraj_average_%s' %str(key),'w')
	for i in range(unitcells):
		for j in range(asymunits):
			if i <=8:
				if j <=8:
					f.write('trajin ../revsym/RevSymm_0%d_0%d.nc %d %d\n' %(i+1,j+1,start,end))
				else:
					f.write('trajin ../revsym/RevSymm_0%d_%d.nc %d %d\n' %(i+1,j+1,start,end))
			else:
				if j <=8:
					f.write('trajin ../revsym/RevSymm_0%d_0%d.nc %d %d\n' %(i+1,j+1,start,end))
				else:
					f.write('trajin ../revsym/RevSymm_0%d_%d.nc %d %d\n' %(i+1,j+1,start,end))
	f.write('average average_%sns.mdcrd \n' %str(key))
	f.close()
	os.system('ptraj '+topo+' <ptraj_average_%s' %str(key))

	#calculate average structure rmsds
	f=open('ptraj_AvgRmsd__%s' %str(key),'w')
	f.write('reference %s\n' %pdb)
	f.write('trajin average_%sns.mdcrd \n' %str(key))
	f.write('rms reference mass out avg_rmsd_sdcn_%s.dat \':2-123 & !(@H=,CA,C,O,N)\' time 0.01 \n' %str(key))
	f.write('rms reference mass out avg_rmsd_bbone_%s.dat \':2-123@CA & !(@H=)\' time 0.01 \n' %str(key))
	f.close()
	os.system('ptraj '+topo+' <ptraj_AvgRmsd__%s' %str(key))


