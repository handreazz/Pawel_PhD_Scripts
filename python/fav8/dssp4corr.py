#! /usr/bin/python
import sys
import os
from numpy import *
import fileinput

unitcells=36
frames=120002
resi=11 #will calculate sec structure content as mean over range of residues from resi to resf
resf=20
ss='G' #G=3-10 helix, H=alpha helix, T=turn

newmatrix=zeros((frames,unitcells))


#first convert dssp output to 0/1 matrix where 'G' is 1 and all else is 0
for i in range(unitcells):
	try:
		d=open('dssp'+str(i+1)+'.dat','r')
	except:
		d=open('dssp0'+str(i+1)+'.dat','r')
	next(d) #skip header row
	frame=0
	for line in d:
		s=line.split()
		del s[0] #erase first column which is the time frame
		counter=0
		for element in s[(resi-1):(resf)]:
			if element==ss:
				counter+=1
		prc=counter/(resf-resi+1.0) *100.0
		newmatrix[frame,i]=prc
		frame+=1
	d.close()
savetxt('dssp4corr',newmatrix,fmt='%6.2f')		
