#! /usr/bin/python
from numpy import *
import ReadAmberFiles as raf

#This replicates what cpptraj does when quasiharmonic calculated

natoms=2
nmodes=6

#mass-weighted covariance matrix is already calculated
cv=genfromtxt('mwcvmat.dat')
l,v=linalg.eig(cv)
s=argsort(l)[::-1]

#convert eigenvalues to frequencies in cm-1
f=zeros((nmodes))
for i in range(len(l)):
	if l[i]<0: f[i]= -108.587*sqrt(-0.6/l[i])
	elif l[i]>0: f[i]= 108.587*sqrt(0.6/l[i])
	else: f[i]=0
l[s]
v[:,s]   #sort columns

#get masses and un-mass weigh the modes
m=raf.prmtop("na.prmtop").Get_Masses()
m=[[i]*3 for i in m]
m=[item for sublist in m for item in sublist] 


for vec in range(v.shape[1]):
	v[:,vec]=v[:,vec]/sqrt(m)



#calculate rmsf fluctuations along modes
CNST=2.776904e-11  #tkbc2*avogadro's  
CONT=1.591549e+07  #(ang/cm / 2pi)
for atom in range(natoms):
	sum, sumx, sumy, sumz=0,0,0,0
	for mode in range(nmodes):
		if f[mode]>=0.01:
			sumx += (v[atom*3,mode]**2 *(1/f[mode]**2) )
			sumy += (v[atom*3+1,mode]**2 *(1/f[mode]**2) )
			sumz += (v[atom*3+2,mode]**2 *(1/f[mode]**2) )
	sum=sumx+sumz+sumy
	print sqrt(array([sumx, sumy, sumz, sum])*CNST)*CONT

#~ import code; code.interact(local=locals())
