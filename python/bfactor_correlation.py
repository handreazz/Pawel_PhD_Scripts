#! /usr/bin/python
import sys
import os
from numpy import *

#Bfactor correlations
#See: /home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/adp/readme


#CALPHA
x=[\
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/bfac_crystal_calpha.dat',\
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/bfac_lat_calpha.dat',\
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/bfac_asu_calpha.dat', \
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/average_density/rmsd/calpha.bfactors'
 ]
 
data1=genfromtxt(x[0])
data2=genfromtxt(x[1])
data3=genfromtxt(x[2])
data4=genfromtxt(x[3])

exp=data1[:,1]
revsym=data2[:,1]
rmsd=data3[:,1]
simrefined=data4[:,1]

#~ import code; code.interact(local=locals())


print corrcoef(exp,rmsd)
print corrcoef(exp,revsym)
print corrcoef(exp,simrefined)


#MEAN SIDECHAIN
x=[\
 '/home/pjanowsk/c/Case/4lzt/RunSi/1.5ms_analysis/bfac_crystal_residue.dat',\
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/bfac_lat_sdch.dat',\
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/revsym/bfac_asu_sdch.dat', \
 '/home/pjanowsk/c/Case/4lzt/4lzt_ff12SB/analysis_i/average_density/rmsd/sdch.bfactors'
 ]
 
data1=genfromtxt(x[0])
data2=genfromtxt(x[1])
data3=genfromtxt(x[2])
data4=genfromtxt(x[3])

exp=data1[:,1]
revsym=data2[:,1]
rmsd=data3[:,1]
simrefined=data4[:,1]

simrefined=[]
for resid in data2[:,0]:
	for row in data4:
		if row[0]==resid:
			simrefined.append(row[1])
			
#~ import code; code.interact(local=locals())



print corrcoef(exp,rmsd)
print corrcoef(exp,revsym)
print corrcoef(exp,simrefined)
