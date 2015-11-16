#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib.pyplot as plt

###
#Produces graphs of water distances to some residue over all unit cells in the crystal simulation.
#Modify this file if you have more than 9999 trajectories(add after line34).
#Modify lines 60+ if you want averaged values (now it's every 10 frames for a 12621 trajectory)
#Modify number of steps in line 60 (simply the number of lines in the files that will be output to waterdist2/
###



trajno=60 #number of trajectories
residuestot=720 #residues in entire supercell
residuesunit=20 #residues in one unit cell
nowaters=4	#no. of water molecules in the 
refatom=7 #sequence no. of residue to which distance measured
water1=721 #no. of first water molecule (this assumes all water molecules are numbered after the peptides)

os.system('mkdir -p waterdist2')
f=open('ptraj_waterdist', 'w')

####write trajins
f.write('trajin ../solvpep.pdb\n')
for i in range(1,10):
	f.write('trajin ../Trajectory/md0'+str(i)+'.nc\n')
for i in range(10,trajno+1):
	f.write('trajin ../Trajectory/md'+str(i)+'.nc\n')
f.write('\n\n\n')

###write backbone distances
for k in range(residuestot/residuesunit):
	refatom1=refatom+k*residuesunit
	for i in range(nowaters):
		watatom=water1+k*nowaters+i
		f.write('distance d'+str(refatom1)+'_'+str(watatom)+' :'+str(refatom1)+'@CA :'+str(watatom)+'@O out waterdist2/d'+str(refatom1)+'_'+str(watatom)+'.dat noimage time 0.2\n')
f.close()	

os.system('ptraj ../solvpep.prmtop <ptraj_waterdist')

#Plot of each unit cell:
fig=plt.figure()
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
plt.suptitle('distance of water molecule to residue '+str(refatom)+' in each unit cell')
for k in range(residuestot/residuesunit):
	refatom1=refatom+k*residuesunit
	ax=plt.subplot(6,6,k+1)
	for i in range(nowaters):
		watatom=water1+k*nowaters+i
		data=genfromtxt('waterdist2/d'+str(refatom1)+'_'+str(watatom)+'.dat')
		x=[]
		y=[]
		for i in range(24001/10):  #this is to get average over each 10 frames (.2ns)
			x.append((data[10*i,0])/10)
			y.append(average(data[10*i:10*i+10,1]))
		plt.plot(x,y)
	for label in ax.xaxis.get_ticklabels():
		label.set_fontsize(4)
	for label in ax.yaxis.get_ticklabels():
		label.set_fontsize(4)
	plt.title(str(k+1),fontsize=4)
	plt.xlabel('ns',fontsize=4)
	plt.ylabel('Angstroms',fontsize=4)	
	plt.ylim(ymax=35)
	plt.xlim(xmax=500)	#modify to trajectory length
plt.show()
#~ #plt.savefig('waterdist.png',dpi=1000,facecolor='gray',aspect='auto')


#plot of all 4 waters:
fig=plt.figure()
for i in range(nowaters):
	for k in range(residuestot/residuesunit):
		watatom=water1+k*nowaters+i
		refatom1=refatom+k*residuesunit
		data=genfromtxt('waterdist2/d'+str(refatom1)+'_'+str(watatom)+'.dat')
		if k ==0:
			y=data[:,1]
		else:
			y=y+data[:,1]
	y=y/(residuestot/residuesunit)
	plt.plot(data[:,0],y)
	plt.xlabel('ns')
	plt.ylabel('Angstroms')
	plt.suptitle('distance of each water to res '+str(refatom)+' averaged over all 36 copies of each water')
plt.show()
