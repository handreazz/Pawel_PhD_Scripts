#! /usr/bin/python
import sys
import os
from numpy import *

#This script is to take the three matrices for the correlation calculation and convert them into 0/1 matrices.

f=open('dihVal18.bin','w')
d=open('dihVal18.new','r')
for line in d:
	newline=[]
	s=line.split()
	for word in s:
		word=float(word)
		value=0
		if word < 0.0:
			word=word+360.0
		#print word
		if word >=140.0:
			#print word
			value=1
		newline.append(value)		
	#print newline
	#x=" ".join(map(str,newline))
	#print x
	f.write(" ".join(map(str,newline)))
	f.write('\n')
f.close()
d.close()


f=open('waterdistribution_shift.bin','w')
d=open('waterdistribution_shift','r')
for line in d:
	newline=[]
	s=line.split()
	for word in s:
		word=float(word)
		value=0
		#~ if word < 0.0:
			#~ word=word+360.0
		if word <= 2.0:
			#print word
			value=1
		newline.append(value)		
	#print newline
	#x=" ".join(map(str,newline))
	#print x
	f.write(" ".join(map(str,newline)))
	f.write('\n')
f.close()
d.close()

f=open('dssp4corr.bin','w')
d=open('dssp4corr','r')
for line in d:
	newline=[]
	s=line.split()
	for word in s:
		word=float(word)
		value=0
		if word >=20.0:
			value=1
		newline.append(value)		
	#print newline
	#x=" ".join(map(str,newline))
	#print x
	f.write(" ".join(map(str,newline)))
	f.write('\n')
f.close()
d.close()
