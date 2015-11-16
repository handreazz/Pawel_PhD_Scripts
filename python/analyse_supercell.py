#! /usr/bin/python
import sys
import os
from numpy import *


### Calculate b-factors for each unit cell and plot.

asymunits=12
topo='../4lztSc_nowat.prmtop'


################
##   Calculate B-factors, rmsd, average structure
################

f=open('ptraj_Analyse_supercell','w')
f.write('trajin ../ptraj/mergtraj_centonpdb_nowat.nc\n')
#~ f.write('rms first mass out rmsd_supercell_bbone.dat :1-756@O5\',C5\',C4\',O4\',C1\',C3\',C2\',O2\',O3\' time 0.01 \n')
#~ f.write('rms first mass out rmsd_supercell_all.dat \':1-756 & !(@H=) & !(:SO4,CON)\' time 0.01 \n')
f.write('atomicfluct out bfac_supercell_calpha.dat \':1-129,140-268,279-407,418-546,557-685,696-824,835-963,974-1102,1113-1241,1252-1380,1391-1519,1530-1658@CA & !(@H=)\' byatom bfactor\n')
f.write('atomicfluct out bfac_supercell_sdch.dat \':1-129,140-268,279-407,418-546,557-685,696-824,835-963,974-1102,1113-1241,1252-1380,1391-1519,1530-1658 & !(@H=,CA,C,O,N)\' byres bfactor\n')
f.close()
os.system('ptraj '+topo+' <ptraj_Analyse_supercell')

###############
#   Combine bfactors
###############


def combinebfactors(ifile, ofile, asymunits):
	data=genfromtxt(ifile)
	atomspercell=shape(data)[0]/asymunits
	combined=zeros((atomspercell,2))
	for i in range(atomspercell):
		a=0
		for j in range(asymunits):
			a+=data[i+j*atomspercell,1]			
		a=a/asymunits
		combined[i,1]=a
		combined[i,0]=i+1
#	savetxt(file[0:file.index('.')]+'_Combined'+file[file.rindex('.'):], combined)
	savetxt(ofile, combined,fmt=['%2d','%6.4f'])

combinebfactors('bfac_supercell_calpha.dat','bfac_supercell_calpha_combined.dat',asymunits)

combinebfactors('bfac_supercell_sdch.dat','bfac_supercell_sdch_combined.dat',asymunits)







