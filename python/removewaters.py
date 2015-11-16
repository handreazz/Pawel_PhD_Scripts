#! /usr/bin/python
import sys
import os
from numpy import *
import fileinput


f=open('reducedwater.pdb','w')

x=range(721,864,4)


for line in fileinput.input('extrawater.pdb'):
	try:
		if int(line[23:26]) not in x:
			f.write(line)
		else:
			continue
		#break
	except ValueError:
		f.write(line)
f.close()
