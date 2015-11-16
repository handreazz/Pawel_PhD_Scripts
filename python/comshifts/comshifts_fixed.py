#! /usr/bin/python
import sys
import os
from numpy import *
import Scientific.IO.NetCDF
from Numeric import * 
from Scientific.IO import NetCDF as Net
from ReadAmberFiles import *

##################################
#ARGUMENTS

#these are the dimensions of the supercell (what PropPDB was given)
ix=3
iy=2	
iz=2

# number of asymmetric units in unit cell
asymunits=1

#directory with the split trajectories
trajpath='../splittrajectories/'

# box dimensions of the crystal supercell. If pressure scaling is isotropic (as this script assumes) you really
# only need the first element (the a or x dimension of the supercell)
box=[81.72, 63.74, 68.46, 88.52 ,108.53 ,111.89] 
pdbwsymtry='/u2/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/asu.pdb'
topo='/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/4lzt_centonpdb_onlyprotein.prmtop'
xtalcoordfile='/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/tmp_i/4lzt_centonpdb_onlyprotein.rst7'
asymatoms=1961
frames=5161


############################################
# Get crystal coordinates, masses, and crystal center of mass (com)
B=rst7(xtalcoordfile)
B.coords=B.Get_Coords()
A=prmtop(topo)
A.masses=A.Get_Masses()
com=COM(B.coords[0:asymatoms,:],A.masses[0:asymatoms])
print 'Crystal center of mass is:'
print com

# calculate the xyz components of an "x", "y", "z" propagation of the unit cell
pdbfile=pdb(pdbwsymtry)
UCbox=pdbfile.Get_Box()
u,invu=CompXfrm(UCbox)
xv=invu[:,0]
yv=invu[:,1]
zv=invu[:,2]


# Get symmetry rotation matrices (smtry) and translation vectors (tr)
smtry,tr =pdbfile.Get_SMTRY()

print 'Number of asymunits provide: %d' %asymunits
print 'Number of symmetry operations in pdb: %d' %(len(smtry))


comshifts=zeros((frames*ix*iy*iz*asymunits,5))
i=1 #counter for the names of the unitcell trajectories
#for each unit cell in the supercell
for x in range(ix):
	for y in range(iy):
		for z in range(iz):
			#calculate the move vector that was applied
			xmove=(x*(xv[0])+y*(yv[0])+z*(zv[0]))
			ymove=(x*(xv[1])+y*(yv[1])+z*(zv[1]))
			zmove=(x*(xv[2])+y*(yv[2])+z*(zv[2]))
			MoveVector=array([xmove,ymove,zmove],dtype=float32)

			for j in range(asymunits):			
				#get symmetry operations for this asym unit
				s=float32(transpose(smtry[j]))
				t=float32(tr[j])
				
				print '\n\nStarting file %02d_%02d.nc' %(i,j+1)
				print 'Move vector is '+ str(MoveVector)
				print 'Symmetry rotation matrix is:'
				print s
				print 'Symmetry tranlation vector is %s' %(str(t))

				#copy the unit cell trajectory to a new taget file
				#read the netcdf file of each unitcell trajectory
				#coords stores the entire coordinates variable which is [frames,atoms,xyzcoords]
				#frames stores the number of frames in the trajectory
				orig_filename=trajpath+'%02d_%02d.nc' %(i,j+1)
				filename='RevSymm_%02d_%02d.nc' %(i,j+1)
				os.system('cp %s %s' %(orig_filename, filename))
				ofile = Net.NetCDFFile(filename, 'a')
				coords=ofile.variables['coordinates']
				frames=coords.shape[0]
				celllen=ofile.variables['cell_lengths']
				
				#iterate over each frame: rescale the atomic coordinates according to boxsize pressure scaling
				for frame in range(frames):
					a=celllen[frame,0] #get a-vector length in current frame
					scale=box[0]/a        
					coords[frame,:,:]=coords[frame,:,:]*scale
					
				#reverse translate to original unit cell by subtracting the translation vector
				coords[:,:,:]=coords[:,:,:]-MoveVector
				#reverse symmetry operate to original asym unit by applying the symmetry translation and rotation
				coords[:,:,:]=dot( (coords[:,:,:]-t),linalg.inv(s) )

				#calculate com shifts relative to crystal
				for frame in range(frames):
					framecoords=coords[frame,:,:]
					framecom=COM(framecoords[0:asymatoms,:],A.masses[0:asymatoms])
					comshift=com-framecom
					euclid_dist=sqrt(dot(comshift,comshift))
					# transform comshift vector into crystal vector (expressed along
					# a,b,c but in angstroms not fractional
					comshift=dot(u,transpose(comshift)) #transoform into fractional
					comshift=comshift*transpose(UCbox[0:3]) #scale fractional to angstroms
					comshifts[frame+(i-1)*frames,0]=frame+1+(i-1)*frames
					comshifts[frame+(i-1)*frames,1]=comshift[0]
					comshifts[frame+(i-1)*frames,2]=comshift[1]
					comshifts[frame+(i-1)*frames,3]=comshift[2]
					comshifts[frame+(i-1)*frames,4]=euclid_dist
				#close file (write to netcdf file)
				ofile.close()
			i+=1
print 'Center of mass mean, min and max shifts:'
print mean(comshifts[:,4])
print min(comshifts[:,4])
print max(comshifts[:,4])
print '\n'
savetxt('com_shifts.dat',comshifts,fmt='%8.5f')



