#! /usr/bin/python
import sys
import os
from numpy import *

inpf=open(sys.argv[1],'r')
outf=open('clean.prmtop', 'w')

#infile= [l for l in inpf.readlines() if l.strip()]

n=0
for line in inpf:
	try:
		#~ if line[0:10]=='%FLAG SCEE':
		if '%FLAG SCEE' in line:
			n=1
		elif '%FLAG SCNB' in line:
			n=1
		elif '%FLAG ATOMIC_NUMBER' in line:
			n=1											
		elif '%FLAG' in line:
			n=0	
	except:
		continue

	if n==1:
		continue
	else:
		outf.write(line)

inpf.close()
outf.close()
		
os.system('mv clean.prmtop %s' %(sys.argv[1]))
