#! /usr/bin/python
import sys
import os
from numpy import *

###
#Modify this file if you have more than 9999 trajectories(add after line34).
###



trajno=60 #number of trajectories, modify lines 27 to 38
residuestot=720 #residues in entire supercell
residuesunit=20 #residues in one unit cell
count=721 #first water residue:
timeblock=400 #divide trajectory into blocks of lenght this many nanoseconds
timestep=.02 #trajectory coord written every this many nanoseconds
blocks=6 #how many timeblock length blocks do you want (counting from end of trajectory)
sb=timeblock/timestep

os.system('mkdir -p distanceouts')
os.system('mkdir -p distmatrices')

f=open('ptraj_backbonedist', 'w')

####write trajins
f.write('trajin ../solvpep.rst7\n')
for i in range(1,10):
	f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n')
for i in range(10,trajno+1):
	f.write('trajin ../Trajectory/md'+str(i)+'.nc\n')
#for i in range(100,1000):
	#f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n')
#for i in range(1000,trajno+1):
	#f.write('trajin ../Trajectory/md'+str(i)+'.nc\n')
#for i in range(trajno-249,trajno+1):
#	f.write('trajin ../Trajectory/md'+str(i)+'.nc\n')
f.write('\n\n\n')


###write backbone distances
#will produce files in ./distanceouts/. File name format: d{residue1}_{residue2}.dat. Each file is list of 
#distances over the trajectory between the CA atom of residue1 and the CA atom of residue2. Distances are measured
#between the CA atoms of each unit cell.
res=1
for k in range(residuestot/residuesunit):
#for k in range(2):	
	last=res+residuesunit
	for i in range(res,last):
		for j in range(i+1,last): #this is because backbone carbons have different name for OME and BOC residues
			if i%10==1:
				atom1='C1'
			elif i%10==0:
				atom1='C'
			else: 
				atom1='CA'
			
			if j%10==1:
				atom2='C1'
			elif j%10==0:
				atom2='C'
			else: 
				atom2='CA'
			
			f.write('distance d'+str(i)+'_'+str(j)+' :'+str(i)+'@'+atom1+' :'+str(j)+'@'+atom2+' out distanceouts/d'+str(i)+'_'+str(j)+'.dat time 0.2\n')
	res+=residuesunit		
f.write('\n\n\n')		
f.close()	

os.system('ptraj ../solvpep.prmtop <ptraj_backbonedist')


os.chdir('distanceouts')
l=os.listdir('.')

###the following section was written to prepare one distance matrix per each unit cell
##for k in range(residuestot/residuesunit):
#for k in range(2):	
	#dmatrix=zeros( (20,20) ) 
	#for i in range(len(l)):
		#x=l[i]
		#if int(x[x.index('d')+1:x.index('_')])<=(k+1)*residuesunit \
		#and int(x[x.index('d')+1:x.index('_')])>(k*residuesunit):
			#dist=genfromtxt(l[i])
			#d=(average(dist[-sb:,1]))-(dist[0:1]) #last 10 time steps (=5 ns)
			#row=(int(x[x.index('d')+1:x.index('_')]))%residuesunit
			#column=(int(x[x.index('_')+1:x.index('.')]))%residuesunit
			#dmatrix[row-1,column-1]=d
			#print l[i]+'  '+str(d)+'  '+str(row)+'  '+str(column)
	#filename='../distmatrices/unitcell'+str(k+1)
	#savetxt(filename, dmatrix)
	#k+=1
	
###this section prepares one huge matrix 720x720
#For each of the CA-CA distances created in the first section above and for each of the time blocks specified
# in the header, a mean of the changes in distance as compared to the crystal distance over the course of 
#the trajectory is calculated and located in the row column of the matrix corresponding to the two residues.
for h in range(1,blocks+1): 
	dmatrix=zeros( (720,720) )
	for i in range(len(l)):
		x=l[i]
		dist=genfromtxt(x)
		d=(average(dist[-sb*h:-sb*h+sb-1,1]))-(dist[0,1]) #last 2500 time steps (=50 ns)
		row=(int(x[x.index('d')+1:x.index('_')]))
		column=(int(x[x.index('_')+1:x.index('.')]))
		dmatrix[row-1,column-1]=d
		#print l[i]+'  '+str(d)+'  '+str(row)+'  '+str(column)
	filename='../bigmatrix_last'+str(h*timeblock)+'to'+str((h-1)*timeblock)+'ns'
	savetxt(filename, dmatrix)
