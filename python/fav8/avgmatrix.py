#! /usr/bin/python
import sys
import os
from numpy import *

###
#takes the distance matrices specified in names and creates a matrix of average values of the
#on diagnonal sub-matrices, in this case 20x20, because the unit cell is 20 residues, so had 
#20 CA atom distances.
###

names=['bigmatrix_last1200to800ns', 'bigmatrix_last1600to1200ns', 'bigmatrix_last2000to1600ns', 'bigmatrix_last2400to2000ns','bigmatrix_last400to0ns','bigmatrix_last800to400ns']

for name in names:
	bigmatrix=genfromtxt(name)
	avgmatrix=zeros((20,20))
	for i in range(20):
		for j in range(i,20):
			#print i,j
			a=[]
			for k in range(36):
				a.append(bigmatrix[i+k*20,j+k*20])
			avg=average(a)
			avgmatrix[i,j]=avg

	savetxt('avg1'+name[9:], avgmatrix)


