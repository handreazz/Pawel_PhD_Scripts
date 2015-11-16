#! /usr/bin/python
import sys
import os
from numpy import *

data=genfromtxt('test.dat')
res=865
atom=11000
H1d=[-0.9570,0,0]
H2d=[0.2400,-0.9270,0]


f=open('addwaters', 'w')
for i in range(9):
	res=865+i
	atom=11000+(i*3)
	O=data[i,5:8]
	H1=data[i,5:8]-H1d
	H2=data[i,5:8]-H2d
	o1=O[1]
	#f.write('ATOM '+str(atom)+'  O   WAT    '+str(res)+'      '+str(O[0])+'  '+str(O[1])+'  '+str(O[2])+'  1.00  0.00          O\n')
	f.write('ATOM  %d  O   WAT   %d      %.3f  %.3f  %.3f  1.00  0.00          O\n' %(atom, res, O[0], O[1], O[2]))
	f.write('ATOM  %d  H1  WAT   %d      %.3f  %.3f  %.3f  1.00  0.00          H\n' %(atom+1, res, H1[0], H1[1], H1[2]))
	f.write('ATOM  %d  H2  WAT   %d      %.3f  %.3f  %.3f  1.00  0.00          H\n' %(atom+2, res, H2[0], H2[1], H2[2]))
	#f.write('ATOM '+str(atom+1)+'  H   WAT    '+str(res)+'      '+str(H1[0])+'  '+str(H1[1])+'  '+str(H1[2])+'  1.00  0.00          H\n')
	#f.write('ATOM '+str(atom+2)+'  H   WAT    '+str(res)+'      '+str(H2[0])+'  '+str(H2[1])+'  '+str(H2[2])+'  1.00  0.00          H\n')
	f.write('TER\n')
