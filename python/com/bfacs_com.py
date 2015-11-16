#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
from Scientific.IO import NetCDF as Net
from Bio.PDB import *

##########################################################################################

##########################################################################################
# COM Method:
# This method reverse symmtery operates each asym unit and then transfers
# that unit's center of mass to align with the crystal asym unit center of
# mass. It will also print the min, mean and max shifts of center of mass between
# the reverse symmetried unit and the crystal. These numbers only make sense
# if the trajectory given is first aligned with the supercell center of mass
# coinciding over the crystal super cell center of mass (use ptraj to do this)
# Arguments:
#	trajfile: name of trajectory
#	asymatoms: number of atoms in the asymetric unit
#	betweenatoms: number of atoms between each asymetric unit (usually crystal solvent)
#	pdbwsymtry: pdb file that has the symmetry information
#	topo: topology of supercell
#	xtalcoordfile: amber rst file with crystal supercell coordinates. This has to be the supercell (or asymunit
#		should work too) but the important thing is that the coordinates of the first asym unit correspond
#		exactly to the pdb coordinates
#	skip: if the trajectory is very large you can read in every this many frames
#
# The way it is set up right now, it also prints an average structure at the end in mdcrd format. Note that
# only the atoms in "asymatoms" variable are used for centre of mass calculation and for rmsd calculation, but the
# average structure includes both "asymatoms" and "betweenatoms" to be comapatible with the UC.prmtop.
##########################################################################################

#######################
#		ARGUMENTS     ###########################################################
#######################

#~ trajfile='/home/pjanowsk/York/hairpin/p2p7e/analysis/mergtraj_cent_52.nc'
trajfile='mergtraj_centonpdb_52_nowat.nc'
asymatoms=1964
betweenatoms=55
pdbwsymtry='../p2p7e.pdb'
topo='p2p7eIa_nowat.prmtop'
xtalcoordfile='p2p7eIa_crystalcoordfile.rst7'
skip=10
boxsizeline= '  94.282  93.144 136.175'

##################################################################################
# Read netcdf file and determine number of frames (based on skip)
ncfile=nc(trajfile)
traj=ncfile.Get_Traj(skip)
frames= traj.shape[0]
print frames

# Get symmetry rotation matrices (smtry) and translation vectors (tr)
pdbfile=pdb(pdbwsymtry)
smtry,tr =pdbfile.Get_SMTRY()

# Get crystal coordinates, masses, and crystal center of mass (com)
B=rst7(xtalcoordfile)
B.coords=B.Get_Coords()
A=prmtop(topo)
A.masses=A.Get_Masses()
com=COM(B.coords[0:asymatoms,:],A.masses[0:asymatoms])

# Create zeros matrix for final coorinates
y=zeros((smtry.shape[0]*frames,asymatoms+betweenatoms,3))

# iatom, fatom are used to select one asym unit at a time to operate on
iatom=0

# comshifts stores the center of mass shift for each asym unit (this is the 
# shift after reverse symmetry. Darrin wanted to know how big they were. It 
# is a measure of lattice disorder
comshifts=zeros((smtry.shape[0]*frames,2))

#reverse symmetry operate each asym unit (all frames at once)
for i in range(smtry.shape[0]):
	###
	fatom=iatom+asymatoms+betweenatoms
	#~ fatom=iatom+asymatoms
	x=traj[:,iatom:fatom,:]
	s=transpose(smtry[i])
	t=tr[i]
	x=dot( (x-t),linalg.inv(s) )
	
	# for each frame move com of asym unit to com of crystal asym unit
	for j in range(frames):
		framecoords=x[j,:,:]
		framecom=COM(framecoords[0:asymatoms,:],A.masses[0:asymatoms])
		comshift=com-framecom
		comshifts[j+i*frames,0]=j+i*frames
		comshifts[j+i*frames,1]=sqrt(dot(comshift,comshift))
		framecoords=framecoords+comshift
		x[j,:,:]=framecoords
	
	#populate y with the new coords	
	y[ (i*frames):((i+1)*frames),:,:]=x
	###
	iatom=fatom
	#~ iatom=fatom+betweenatoms
#debugging
#~ for i in range(smtry.shape[0]):
	#~ print y[i*frames+10,5,:]
	#~ print y[i*frames+12,5,:]
#~ print "\n"	
print 'Center of mass mean, min and max shifts:'
print mean(comshifts[:,1])
print min(comshifts[:,1])
print max(comshifts[:,1])
print '\n'

avg=AverageStructure(y)	
bfacs=BFactors(y,avg)
print 'COM method bfacs:'
print bfacs
print '\n'
savetxt('bfac_com.txt',bfacs,fmt='%8.2f')

print 'RMSD: '
print RMSD(avg[0:asymatoms,:],B.coords[0:asymatoms,:],A.masses[0:asymatoms])
print '\n'

printmdcrd(avg,boxsizeline,'avg_com_rmsd.mdcrd')

########################################################################

#########################################################################
## AsymUnitCOM method:
## For each frame, alings the com of the first asym unit in the supercell
## to the crystal asym unit. Than reverses symmetry on all asym units and 
## calculates b-factors without any more center of mass shifting. Thus
## lattice disorder is preserved.
#########################################################################

##create zeros matrix for new coordinates
#y=zeros((smtry.shape[0]*frames,asymatoms,3))

##translate supercell so that com of 1st asym unit is aligned with crystal
#for i in range(frames):
	#frame=traj[i,:,:]
	#asym1coords=frame[0:asymatoms]
	#asym1masses=A.masses[0:asymatoms]
	#asym1com=COM(asym1coords,asym1masses)
	#comshift=com-asym1com
	##~ print comshift
	#frame=frame+comshift
	#traj[i,:,:]=frame

	
#iatom=0
## reverse symmetry operate each asym unit and save to y array
#for i in range(smtry.shape[0]):
	#fatom=iatom+asymatoms
	#x=traj[:,iatom:fatom,:]
	#s=transpose(smtry[i])
	#t=tr[i]
	#x=dot( (x-t),linalg.inv(s) )
	#y[ (i*frames):((i+1)*frames),:,:]=x
	#iatom=fatom+betweenatoms

##debugging
##~ for i in range(smtry.shape[0]):
	##~ print y[i*frames+10,5,:]
	##~ print y[i*frames+12,5,:]
##~ print "\n"	
##~ for i in range(smtry.shape[0]):
	##~ print y[i*frames+10,500,:]
##~ print "\n\n"
	

#avg=AverageStructure(y)	
#bfacs=BFactors(y,avg)
#print 'AsymUnitCOM method bfacs:'
#print bfacs
#print '\n'
#savetxt('bfac2.txt',bfacs,fmt='%8.2f')

#print 'RMSD: '
#print RMSD(avg,B.coords[0:asymatoms,:],A.masses[0:asymatoms])
#print '\n'

########################################################################

###################################################################################
# This was a method that is not useful. The idea was to rmsd fit the first        #
# asymmetric unit to the crystal asym unit (using ptraj). Then perform reverse    #
# symmetry. However this inflates the b-factors artificially: while b-factors for #
# asym unit 1 are minimized, the rotation of the entire supercell subsequently    #
# increases b-factors of other asym units.                                        #
###################################################################################

#trajfile='mergtraj_cent_52_stripped_tr.nc'
#asymatoms=1964
#betweenatoms=55
#pdbwsymtry='p2p7e.pdb'
#topo='p2p7eIa.prmtop'
#xtalcoordfile='p2p7eIa_tr.rst7'

#ncfile=nc(trajfile)
#frames=ncfile.Get_Frames()
#traj=ncfile.Get_Traj()

#pdbfile=pdb(pdbwsymtry)
#smtry,tr =pdbfile.Get_SMTRY()

#y=zeros((smtry.shape[0]*frames,asymatoms,3))
#iatom=0
#for i in range(smtry.shape[0]):
	#fatom=iatom+asymatoms
	#x=traj[:,iatom:fatom,:]
	#s=transpose(smtry[i])
	#t=tr[i]
	#x=dot( (x-t),linalg.inv(s) )
	#y[ (i*frames):((i+1)*frames),:,:]=x
	#iatom=fatom+betweenatoms

##~ for i in range(smtry.shape[0]):
	##~ print y[i*frames+10,5,:]
##~ print "\n"	
##~ for i in range(smtry.shape[0]):
	##~ print y[i*frames+10,500,:]
##~ print "\n\n"
	
#avg=AverageStructure(y)	
#bfacs=BFactors(y,avg)
#print bfacs
#print bfacs.shape
