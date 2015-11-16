#! /usr/bin/python

from numpy import *


x=genfromtxt('200c_nofit.summary.dat')

f=open('200c_fracs.dat','w')
f.write("#Cluster   Frames           Frac  \n")

for i in range(200):
	cluster=i+1
	clust_frames=x[i,1]
	total_frames=float(sum(x[:,1]))
	freq=clust_frames/total_frames
	f.write("%8i   %6i     %10.8f\n" %(i, clust_frames, freq))
