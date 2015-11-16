#! /usr/bin/python

from numpy import *

x=genfromtxt('dihVal18.bin')
n=round(sum(x)/(x.shape[0]*x.shape[1]),2)*100
print ("Dihedral ValB8 in gauche(-) %2.f%%" %n) 
#print  x.shape


x=genfromtxt('waterdistribution_shift.bin')
n=round(sum(x)/(x.shape[0]*x.shape[1]),2)*100
print ("Dry water state \t %2.f%%" %n)
#print x.shape


x=genfromtxt('dssp4corr.bin')
n=round(sum(x)/(x.shape[0]*x.shape[1]),2)*100
print ('Three-10 helix propensity  %2.f%%' %n)
#print x.shape

