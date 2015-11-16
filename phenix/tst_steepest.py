#! /usr/bin/python
#import ReadAmberFiles as raf
import numpy as np
import phenix_amber_interface as ext
import argparse
from scitbx.array_family import flex


def getstd():
	R=[]
	for iter in range(100):
		i=2*np.random.randn(2)
		r=np.sqrt(i[0]**2+i[1]**2)
		R.append(r)
	return np.array(R).std()
	

def meanstd():
	sum=0
	for i in range(100):
		sum+=getstd()
	return sum/100.

def bstrp():
	sums=0	
	for i in range(100):
		sums+=meanstd()
	print sums/100	 	
	#~ 
	
#~ x=0
#~ for jiter in range(100):
	#~ x+=getstd()
#~ print x/100.0	
	
#~ print np.sqrt(3)
#~ print np.sqrt(1.0/3.0)

#~ mean=[0,0,0]
#~ cov=[[2.25,0,0],[0,2.25,0],[0,0,2.25]]
#~ x=0
#~ for i in range (1000):
	#~ sample=np.random.multivariate_normal(mean,cov,100)
	#~ x+=np.std(np.array([np.linalg.norm(r) for r in sample]))
#~ print x/1000


def jiggle(coords2):
	for atom in range(len(coords2)):
		coords2[atom]=coords2[atom]+(.15*np.random.randn(3))
	return	coords2


def run(pdbfile,prmtopfile,crdfile):
#	coords=raf.pdb(pdbfile).Get_Coords()
	#~ coords=jiggle(coords)

	U=ext.uform(prmtopfile, crdfile)

	gradients=flex.double(150)
	print gradients
	gradients_flex=ext.ExtractVec(gradients)

	n=list(coords.flatten())
	sites_cart_c=ext.ExtractVec2(n)
        nowendithere
	gradients_c=ext.ExtractVec(gradients)
	target_c=ext.ExtractVec(target)
	ext.callMdgx(sites_cart_c, gradients_c, target_c, U)
	gradients=flex.vec3_double(gradients_c)*-1
	target= flex.double(target_c)	
	
	


if __name__ == "__main__" :
        parser = argparse.ArgumentParser()
        parser.add_argument("-pdb", help="name of pdb file", default="vAla3_minimized.pdb")
        parser.add_argument("-prmtop", help="name of topology file", default="vAla3.prmtop")
        parser.add_argument("-crd", help="name of coordinate file", default="vAla3_minimized.rst7")
        args = parser.parse_args()
        run(args.pdb,args.prmtop, args.crd)



