#! /usr/bin/env python

import sys

data=[]
f=open("summary.txt","r")
for line in f.readlines():
	data.append(line.strip().split())
f.close()

f=open('data.txt','w')
f.write('NODES   SECONDS\n\n')
for i in range(len(data)):
	try:
		if data[i][0]=='NUMBER':
			f.write('%2s      %s\n' %(data[i][3],data[i+2][5]))
	except:
		continue
f.close()

