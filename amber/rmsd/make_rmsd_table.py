#! /usr/bin/python
import sys
from numpy import *
import commands

# SET ARGUMENTS
unitcells=12
asymunits=1
frames=int(commands.getoutput('wc -l rmsd_monomer_all.dat').split()[0])/(unitcells*asymunits)
print frames


def ProcessRmsd(ifile,ofile,frames,total_monomers):
	f=open(ofile,'w')
	data=genfromtxt(ifile)
	assert len(data)%total_monomers == 0, "number of frames not a multiple of total_monomers"
	x=array([])
	f.write('    time     mean      std     rmsds_of_each_monomer\n')
	for i in range(frames):
		for j in range(total_monomers):
			x=append(x,data[i+j*frames,1])
		f.write('%7.2f   ' %data[i,0])
		f.write('%7.3f   %7.3f   ' %(mean(x), std(x,ddof=1)))
		### If you want sqrt of the mean of squares in stead of simple mean:
		# f.write('%7.3f   %7.3f   ' %(sqrt(mean(x**2)), std(x,ddof=1)))
		for value in x:
			f.write('%7.3f   ' %value)
		f.write('\n')
		x=array([])
	f.close()

ProcessRmsd('rmsd_monomer_all.dat','rmsd_monomer_all_table.dat',frames,unitcells*asymunits)
