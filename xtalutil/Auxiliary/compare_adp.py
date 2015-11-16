#!/usr/bin/env python
import os
from numpy import *
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#######################################################################	
# Calculate angles between X-axis and the principle axes of both the  #
# experimental and simulation anisotropic ellipsoids. Results go to   #
# output file (default=out.pdb). Also calculates the anisotropy (ratio#
# of major/minor princple axes for both experimental and simulation   #
# ANISOU tensors. This is printed in the last to columns of the out   #
# file. Optionally modify the plot() function to plot the angles      # 
# (filter for specific atom names)                                    #
#                                                                     #
# Arguments:                                                          #
#     - e experimental pdb with ANISOU                                #
#     - s simulation pdb with ANISOU                                  #
#     - o output file name.                                           #
# Example usage:                                                      #
#    ./compare_adp.py -e 4lzt.pdb -s 4lzt_adp.pdb                     #
#######################################################################

def getpdb(filename):
	pdb=[]
	with open(filename) as f:
		for line in f:
			if line[0:6] == 'ANISOU':
				pdb.append(line)
	return pdb

def principle_axes(line):
	ani_tensor=zeros((3,3))
	ani_tensor[0,0]=int(line[28:35])
	ani_tensor[1,1]=int(line[35:42])
	ani_tensor[2,2]=int(line[42:49])
	ani_tensor[0,1]=int(line[49:56])
	ani_tensor[1,0]=int(line[49:56])
	ani_tensor[0,2]=int(line[56:63])
	ani_tensor[2,0]=int(line[56:63])
	ani_tensor[1,2]=int(line[63:70])
	ani_tensor[2,1]=int(line[63:70])
	eigenValues,eigenVectors = linalg.eig(ani_tensor)
	idx = eigenValues.argsort()[::-1] 
	eigenValues = eigenValues[idx]
	anisotropy=eigenValues[0]/eigenValues[2]  
	eigenVectors = eigenVectors[:,idx]
	B=(ani_tensor[0,0]+ani_tensor[1,1]+ani_tensor[2,2])/10000*8/3*pi*pi
	return eigenVectors[:,0], anisotropy,B

def angle_between_vectors(px,py):
	c = dot(px,py)/linalg.norm(px)/linalg.norm(py) 
	angle = arccos(c)
	#special case if parallel/antiparallel
	if isnan(angle):
		if (v1_u == v2_u).all():
			angle=0.0
		else:
			angle=np.pi
	# for fluctuation direction, put on [0,pi/2] interval		
	while (angle<=0):
		angle+=pi/2
	while angle>pi/2:
		angle-=pi/2    
	# return in degrees
	return angle*180./pi

def print_out(data,o_filename):
	f=open(o_filename,'w')
	f.write('resid     atom    u11exp  u22exp  u33exp   u12exp  u13exp  u23exp  Bexp     u11sim  u22sim  u33sim  u12sim  u13sim  u23sim  Bsim   uang_[100]exp  ang_[100]sim  ang_exp_sim    anis_exp    anis_sim\n')
	for i in data:
		f.write("%4s      %4s  %7d %7d %7d %7d %7d %7d   %6.2f  %7d %7d %7d %7d %7d %7d  %6.2f   %6.3f        %6.3f        %6.3f         %6.3f         %6.3f\n" %(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20]) )
	f.close()

def plot(data):
	# filter data by atom name (comment out if all atoms)
	data=array([i[2:] for i in data if i[1].strip()=='CZ'])
	print data
	plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
	plt.rc('axes',linewidth=3)
	plt.rc('legend', fontsize=20) 
	plt.rc('lines', markeredgewidth=2)
	plt.rc('xtick.minor',size=5)
	plt.rc('xtick.major',size=10)
	plt.rc('lines', linewidth=3) 
	# angles to x-vector
	#~ plt.plot(data[:,0],'r')
	#~ plt.plot(data[:,1],'b')
	# angles between exp and sim
	plt.plot(data[:,2],'g')
	plt.title("4lzt_i angles between x-axis and principle axis of anisotropic tensor (C-alpha atoms)")
	plt.legend(["experimental", "simulation"],bbox_to_anchor=(0, 0.0, .99, .99))
	plt.show()
	#~ plt.savefig('adp_axes.pdf')
	print corrcoef(data[:,0],data[:,1])


fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)


def run(exp_filename, sim_filename, o_filename):
	exp_pdb=getpdb(exp_filename)
	sim_pdb=getpdb(sim_filename)
	xvector=array([1,0,0])
	
	data=[]
	for eline in exp_pdb:
		for sline in sim_pdb:
		  if eline[16] in ['A',' ']:
			if eline[22:26] == sline[22:26] and eline[12:16] == sline[12:16]:
				ep, e_ani, e_B=principle_axes(eline)
				sp, s_ani, s_B=principle_axes(sline)
				data.append([eline[22:26], eline[12:16], \
					int(eline[28:35]), int(eline[36:42]), int(eline[43:49]), \
					int(eline[50:56]), int(eline[57:63]), int(eline[64:70]), \
					e_B, \
					int(sline[28:35]), int(sline[36:42]), int(sline[43:49]), \
					int(sline[50:56]), int(sline[57:63]), int(sline[64:70]), \
					s_B, \
					angle_between_vectors(xvector,ep),  \
					angle_between_vectors(xvector,sp) , angle_between_vectors(ep,sp), \
					e_ani, s_ani]  )
	#~ import code; code.interact(local=locals())				 
	print_out(data,o_filename)
	#~ plot(data)
	#~ 
	
		
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--exp_pdb", help="name of pdb file with experimental ADPs")
	parser.add_argument("-s", "--sim_pdb", help="name of pdb file with simulation ADPs")
	parser.add_argument("-o", help="output pdb file name", default="out.dat")	
	args = parser.parse_args()
	run(args.exp_pdb, args.sim_pdb, args.o)
