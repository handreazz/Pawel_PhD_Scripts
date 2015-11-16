#! /usr/bin/python
import sys
import os
from numpy import *


pdbfile='1rpgK.pdb'


f=open(pdbfile,'r')
infile= [l for l in f.readlines() if l.strip()]
f.close()

f=open('x.pdb','w')

#heavy atom restraints
for line in infile: 
	line=list(line)
	#~ print line[17:20]
	if len(line)<=11:
		#~ print line
		pass
	elif line[0:3]!=['A', 'T', 'O']:
		pass
	elif line[17:20]==['W', 'A', 'T']:
		line[62]='0'
	elif line[13]=='H':
		line[62]='0'
	elif line[12]=='H':
		line[62]='0'	
	elif line[17:20]==['C', 'l', '-']:
		line[62]='0'		
	else:
		line[62]='1'
	#~ print line		
	line="".join(line)
	f.write(line)

f.close()				
