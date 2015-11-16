#! /usr/bin/python
import sys
import os
from numpy import *

#read mdcrd file, return vector of all coordinates and vector of boxsize (last line of file)
def readmdcrd(filename):
	with open(filename) as f:
		x = f.readlines()
	boxsizeline=x[len(x)-1]
	x=x[1:len(x)-1]  #delete first and last line of file
	coords =[]
	for line in x:
		coords.extend(line.split())
	return coords, boxsizeline
#will tranform the vector of all the coordinates into a vector of new coordinates based on the movevector (x, y, z translation) provided	
def transformcoords(coords_old,MoveVector):
	coords_new=[]
	atoms=len(coords_old)/3.0
	for atom in range(int(atoms)):
		x_old=float(coords_old[atom*3+0])
		y_old=float(coords_old[atom*3+1])
		z_old=float(coords_old[atom*3+2])
		x_new, y_new, z_new = x_old-MoveVector[0], y_old-MoveVector[1], z_old-MoveVector[2]
		coords_new.extend([x_new,y_new,z_new])
	return coords_new	

#will take a vector of coordinates and a boxsize line and create a mdcrd format file with it)
def printmdcrd(coords_new, boxsizeline,filename):
	f=open(filename,'w')
	f.write('crystal unit cell reverse transformed by pawel\n')
	i=1
	for coord in coords_new:
		f.write('%8.3f' %coord)
		if i==10:
			f.write('\n')
			i=0
		i+=1
	f.write('\n'+boxsizeline)
	f.close()
##################################
#MODIFY HERE

#these are the dimensions of the supercell (what PropPDB was given)
ix=4
iy=3
iz=3
#these are the lines of the U matrix (xyz components of an "x", "y", "z" propagation of the unit cell)
xv=array([10.8020, 0, 0])
yv=array([-0.9019, 16.3361, 0])
zv=array([-1.7204, -8.0479, 15.8430])
######################################



i=0
#for each unit cell in the supercell
for x in range(ix):
	for y in range(iy):
		for z in range(iz):
			#calculate the move vector that was applied
			xmove=(x*(xv[0])+y*(yv[0])+z*(zv[0]))
			ymove=(x*(xv[1])+y*(yv[1])+z*(zv[1]))
			zmove=(x*(xv[2])+y*(yv[2])+z*(zv[2]))
			MoveVector=[xmove,ymove,zmove]
			
			#read in coords from mdcrd file
			coords_old, boxsizeline=readmdcrd('../rmsf/unitcells/average_%d.mdcrd' %(i+1))
			#calculate coords in original unit cell by subtracting the move vector
			coords_new=transformcoords(coords_old, MoveVector)
			#print new mdcrd file
			printmdcrd(coords_new, boxsizeline, 'ReversTrans_avg_%02d.mdcrd' %(i+1))
			

			i+=1

###for just one unitcell/debugging
#~ i=13
#~ #for each unit cell in the supercell
#~ for x ==2:
	#~ for y ==2:
		#~ for z==2:
			#~ #calculate the move vector that was applied
			#~ xmove=(x*(xv[0])+y*(yv[0])+z*(zv[0]))
			#~ ymove=(x*(xv[1])+y*(yv[1])+z*(zv[1]))
			#~ zmove=(x*(xv[2])+y*(yv[2])+z*(zv[2]))
			#~ MoveVector=[xmove,ymove,zmove]
			#~ 
			#~ #read in coords from mdcrd file
			#~ coords_old, boxsizeline=readmdcrd('../rmsf/unitcells/average_%d.mdcrd' %(i+1))
			#~ #calculate coords in original unit cell by subtracting the move vector
			#~ coords_new=transformcoords(coords_old, MoveVector)
			#~ #print new mdcrd file
			#~ printmdcrd(coords_new, boxsizeline, 'ReversTrans_avg_%02d.mdcrd' %(i+1))
			





###DEBUGGING STUFF
			#~ print i
			#~ print x, y, z
			#~ print coords_new

				#x_new = x_old-xmove
			#print boxsizeline
			#print atoms
			
			#~ print "unitcell "+str(i)
			#~ print 'xmove= '+str(xmove)

			#print 'average_%d.mdcrd' % (i)

