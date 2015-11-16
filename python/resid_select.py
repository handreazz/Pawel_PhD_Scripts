#! /usr/bin/python

from __future__ import print_function

a=1
for i in range(6):
	if i!=0:
		print("+", end='')
	print( "%s-%s" %(1+i*139*2,1+i*139*2+138), end='')
print("\n", end='')
