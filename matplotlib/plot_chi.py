#! /usr/bin/python
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
import sys
from smooth_signal import smooth

#PLOT phi and psi angles of entire protein on separate plots.
#Input read from cpptraj output. Files saved to PerResidue folder


#plot settings
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20) 
plt.rc('lines', markeredgewidth=2)
plt.rc('xtick.minor',size=9)
plt.rc('xtick.major',size=10)
plt.rc('lines', linewidth=2) 
colors=['#F86606',\
 '#CC0000', \
 '#F3EF02', \
 '#5DF304', \
 '#4E9A06', \
 '#C4A000', \
 '#729FCF', \
 '#0618F4', \
 '#06EFF4', \
 '#A406F4', \
 '#F4069D', \
 '#936F70']  

#read experimental values
f=open('chi.dat','r')
tmp=f.readline()
angle_names=tmp.strip().split()[1:]
tmp=f.readline()
angles_exp=tmp.strip().split()[1:]
f.close()

#read simulation values
chis=genfromtxt('chi.dat',skip_header=2)
chis=chis[:,1:]
save('outfile',chis)
#~ chis=load('outfile.npy')
assert (len(angle_names)==chis.shape[1])
for angle in range(len(angle_names)):
	angle_name=angle_names[angle]
	angle_exp=float(angles_exp[angle])
	fig=plt.figure(figsize=(16, 12))
	ax = fig.add_subplot(111)
	ax.hist(chis[:,angle], 360, range=[-180,180], facecolor='black', alpha=1.00, normed=False, histtype='stepfilled')
	ax.plot([angle_exp,angle_exp],[0,3000],'r',linewidth=4)
	plt.ylim((0,2500))
	plt.title("Residue "+angle_name.split(':')[1], fontsize=28)
	#~ ax.legend(bbox_to_anchor=(0, 0, 1.08, 1))
	plt.xlabel(r'$\chi$ angle (degrees)', fontsize=28, labelpad=10)
	plt.ylabel(r'count (total=61932)',fontsize=28, labelpad=10)
	plt.savefig('chi%02d.png' %(int(angle_name.split(':')[1])) ) 
	

