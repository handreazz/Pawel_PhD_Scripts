#! /usr/bin/env python

import sys
import fileinput
import os

f=open('bfactors','r')
lines=f.readlines()
f.close()

f=open('test','w')


for line in range(len(lines)):
		f.write(str(line+1)+'\t'+lines[line])
f.close()

os.system('mv test 4lzt.bfactors')

