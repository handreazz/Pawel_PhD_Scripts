#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

topo_dir='../UC.prmtop'
asym_units=12
unit_cells=1
step=10

topo=prmtop(topo_dir)
residues=topo.Get_Residues()

chi={'U':['O4\'','C1\'','N1','C2'],'U3':['O4\'','C1\'','N1','C2'],'U5':['O4\'','C1\'','N1','C2'],\
	 'C':['O4\'','C1\'','N1','C2'],'C3':['O4\'','C1\'','N1','C2'],'C5':['O4\'','C1\'','N1','C2'],\
	 'A':['O4\'','C1\'','N9','C4'],'A3':['O4\'','C1\'','N9','C4'],'A5':['O4\'','C1\'','N9','C4'],\
	 'G':['O4\'','C1\'','N9','C4'],'G3':['O4\'','C1\'','N9','C4'],'G5':['O4\'','C1\'','N9','C4'],\
	 }

#~ for residue in range(len(residues)):
	#~ if residues[residue] not in chi:
		#~ print 'skipping %s_%d' %(residues[residue],residue)
	#~ else:
		#~ atoms=chi[residues[residue]]
		#~ for uc in range(unit_cells):
			#~ for asym in range(asym_units):
				#~ f=open('cptraj_dihedral','w')
				#~ f.write('parm %s\n' %topo_dir)
				#~ f.write('trajin ../splittrajectories/%02d_%02d.nc\n' %(uc+1,asym+1))
				#~ f.write('dihedral :%d@%s :%d@%s :%d@%s :%d@%s out X%02d_%02d_%02d.dat\n' %(residue+1,atoms[0],residue+1,atoms[1],residue+1,atoms[2],residue+1,atoms[3],residue+1,uc+1,asym+1))
				#~ f.close()
				#~ print 'asym unit %d' %asym
				#~ os.system('cat cptraj_dihedral')
				#~ os.system('cpptraj <cptraj_dihedral >tmp')

#####################################
# GENERAL PLOT SETTINGS             #
#####################################
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20)
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


data=genfromtxt('X%02d_%02d_%02d.dat' %(1,1,1),skip_header=1)
frames=data.shape[0]
avg_dist=zeros(frames/step)
 
for residue in range(len(residues)):
	if residues[residue] not in chi:
		print 'skipping %s_%d' %(residues[residue],residue)
	else:
		fig=plt.figure(figsize=(16, 12))
		ax = fig.add_subplot(111)
		for uc in range(unit_cells):
			for asym in range(asym_units):
				unit = uc*int(asym_units)+asym
				data=genfromtxt('X%02d_%02d_%02d.dat' %(residue+1,uc+1,asym+1),skip_header=1)
				frames=data.shape[0]
				angle_cryst=data[0,1]
				x,y =[],[]
				for j in range(frames/step):  #this is to get average over each 10 frames (.1ns)
					x.append((data[step*j,0]))
					angle=average(data[step*j:step*j+step,1])
					if angle >=165.0:
						angle=angle-180.0
					y.append(angle)
				
						
				#~ ax.plot(data[:,0],data[:,1],colors[unit], linewidth=1,label=str(unit+1))
				ax.plot(x,y,colors[unit], linewidth=2,label=str(unit+1))
				avg_dist=avg_dist+y
		x=[1,frames]
		print x
		y=[angle_cryst,angle_cryst]
		print y
		ax.plot(x,y,'k',linewidth=1,label='crystal')	
		for label in ax.xaxis.get_ticklabels():
			label.set_fontsize(24)
		for label in ax.yaxis.get_ticklabels():
			label.set_fontsize(24)
		
		plt.title('Residue %d %s' %(residue+1,residues[residue]),fontsize=28)
		plt.xlabel('Time (ns)',fontsize=28, labelpad=10)
		#ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
		plt.ylabel(r"Angle ($degrees$)",fontsize=28, labelpad=10)
		plt.ylim((-190,190))
		#plt.xlim(xmax=51)	#modify to trajectory length
		ax.yaxis.set_ticks_position('left')
		ax.xaxis.set_ticks_position('bottom')
		for line in ax.get_xticklines() + ax.get_yticklines():
			line.set_markeredgewidth(4)
			line.set_markersize(10)
		from matplotlib.font_manager import fontManager, FontProperties
		font=FontProperties(size=18)
		ax.legend()
		ax.legend(bbox_to_anchor=(0, 0, .99, .99),prop=font,ncol=4)
		
		plt.savefig('%02d.png' %(residue+1)) 
