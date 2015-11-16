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
f=open('PhiPsi_ASU.dat','r')
tmp=f.readlines()
angle_names=tmp[0].split()[1:]
angle_exp=tmp[1].split()[1:]
#read simulation values
#~ sys.exit()
davg=genfromtxt('PhiPsi_ASU.dat')
dtmp1=zeros((7426,258))
for asu in range(12):
	tmp=genfromtxt('PhiPsi_%02d_01.dat' %(asu+1))[:,1:]
	if asu==0:
		angle_sim=array([tmp])		
	else:
		angle_sim=vstack((angle_sim,[tmp]))
		print angle_sim.shape
save('outfile',angle_sim)
#once save to .npy file no need to reload
angle_sim=load('outfile.npy')
print angle_sim.shape
#for each phi/phi angle
for angle in range(257):
	
	#get experimental name and value
	c_name=angle_names[angle]
	c_exp=float(angle_exp[angle])
	fig=plt.figure(figsize=(16, 12))
	ax = fig.add_subplot(111)
	ax.plot([0,800],[0,0],'k')
	#for each asu
	for asu in range(12):
		#get simulation value
		c_sim=angle_sim[asu,::10,angle]
		#zero around experimental value
		c_sim=c_sim-c_exp
		#wrap values <-180 or >180
		index=c_sim>180
		c_sim[index]=c_sim[index]-360
		index=c_sim<-180
		c_sim[index]=c_sim[index]+360
		#apply hanning smoother		
		ax.plot(smooth(c_sim),colors[asu],label=asu+1)
		#~ ax.plot(c_sim,label=asu)
		plt.title(c_name, fontsize=28)
		ax.legend(bbox_to_anchor=(0, 0, 1.08, 1))
		plt.xlabel('time', fontsize=28, labelpad=10)
		plt.ylabel(r"degrees",fontsize=28, labelpad=10)
		plt.ylim((-180,180))
	##~ plt.show()
	plt.savefig('PerResidue/%s_%s.png' %(c_name.split(':')[1],c_name.split(':')[0])) 
	print angle
print "i am done"
