#! /usr/bin/python
import sys
import os
from numpy import *

#Take waterdistribution file and swaps columns so that water states are in the column whose number corresponds to the UC that that water state affects.



states=genfromtxt('../ChannelWater/waterdistribution')
shiftst=zeros((120002,36))
for i in range(1,37):
	if i%3==1: 
		j=i+2
	elif i%3==0 or i%3==2:
		j=i-1
	shiftst[:,i-1]=states[:,j-1]

savetxt('waterdistribution_shift',shiftst,fmt='%d')
