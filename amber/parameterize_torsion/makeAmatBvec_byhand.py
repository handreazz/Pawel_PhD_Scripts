#! /usr/bin/python
import sys
import os
from numpy import *

#####
#Given a Gaussian output file and and a two column file (BLYPEN.txt) with 
#quantum energies for various conformations, will get coordinates from
#the Gaussian output and calculate the energy components, subtract them 
#from BLYPEN to form the b vector. Then look at the angles to be fitted 
#and create a matrix A of their values (assuming the formula for the 
#dihedral energy is k*cos(theta) and we want k. These
#outputs will be used for the llsp.m fitting.
####

#Read in gaussian output file. Find the optimized parameters section.
#Return dictonary of atom coordinates, bond-angle-dihedral values and distance matrix.
def ReadGvFile(fname):
	y='                           !   Optimized Parameters   !\n'

	f=open(fname, 'r')
	x=f.readlines()
	f.close()

	for i, line in enumerate(x):
		if line==y:
			lineno=i
	
	params={}
	for i in range(5,51):
		line=(x[lineno+i]).split()
		key=line[1]
		value=float(line[3])
		params[key]=value
		
	coords={}
	for i in range(59,70):
		line=(x[lineno+i]).split()
		key=int(line[0])
		value=[float(line[3]), float(line[4]), float(line[5])]
		coords[key]=value
	
	distmat=zeros((11,11))
	for i in range(73,84):
		line=x[lineno+i].strip().split()
		for j in range(11):
			try:
				distmat[i-73,j]=line[j+2]
			except:
				pass
	for i in range(86,91):
		line=x[lineno+i].strip().split()
		for j in range(11):
			try:
				distmat[i-86+6,j+5]=line[j+2]
			except:
				pass
	b=distmat.transpose()
	distmat=distmat+b
	return params, coords, distmat

#Takes the BLYPEN.txt file (total energies from gaussian) and puts it on the x-axis	
def convertB(Babs):
	x=min(Babs[:,1])
	rows=Babs.shape[0]
	for i in range(rows):
		Babs[i,1]=Babs[i,1]-x #Center B on 0 by subtracting the mean value of B from each term (here 1.5 is approximate)
	return Babs
	
#Convert dictionary of atom number coordinates to atomname x, y, z coordinates
def namecoords(coords, atnames):
	coordn={}
	for (key,value) in coords.items():
		coordn[atnames[key]+'x']=value[0]
		coordn[atnames[key]+'y']=value[1]
		coordn[atnames[key]+'z']=value[2]
	return coordn

#read the value of the B matrix at a given position
def GetTotalGvEnergy(pos,B):
	Tenergy = B[pos,1]
	return Tenergy

#Calculate total bond energy for the list of bonds given (names, numbers, gaussian name, spring constant, eq. length)
def CalcBondEnergy(coords):
	###########
	#  BONDS  #  k*d**2
	###########
	Bonds=[ \
	['H1-C1', '2-3', 'R5',   340.0,    1.090], \
	['H2-C1', '2-4', 'R6',   340.0,    1.090], \
	['H3-C1', '2-5', 'R7',   340.0,    1.090], \
	['H4-C2', '6-7', 'R8',   340.0,    1.090], \
	['H5-C2', '6-8', 'R9',   340.0,    1.090], \
	['H6-C2', '6-9', 'R10',  340.0,    1.090], \
	['C1-AS', '1-2', 'R1',   400.0,    1.945], \
	['C2-AS', '1-6', 'R2',   400.0,    1.945], \
	['O1-AS', '1-10', 'R3',   400.0,    1.640], \
	['O2-AS', '1-11', 'R4',   400.0,    1.640], \
	]
	TotBondE=0
	for i in Bonds:
		atom=i[1].split('-')
		atom=[int(x) for x in atom]
		r=[coords[atom[0]][0]-coords[atom[1]][0], \
		coords[atom[0]][1]-coords[atom[1]][1], \
		coords[atom[0]][2]-coords[atom[1]][2]]
		magnr=math.sqrt(r[0]**2+r[1]**2+r[2]**2)
		rdiff=magnr-i[4]
		k=i[3]
		bondE=k*rdiff**2
		TotBondE=TotBondE+bondE
	return TotBondE

#Calculate total angle energy for the list of angles given (names, numbers, gaussian name, spring constant, eq. length)
def CalcAngleEnergy(coords):
	###########
	#  ANGLES #  k*theta**2
	###########
	Angles=[ \
	['H1-C1-AS', '1-2-3',    'A7',       80.0,      109.5], \
	['H2-C1-AS', '1-2-4',    'A8',       80.0,      109.5], \
	['H3-C1-AS', '1-2-5',    'A9',       80.0,      109.5], \
	['H4-C2-AS', '1-6-7',    'A13',      80.0,      109.5], \
	['H5-C2-AS', '1-6-8',    'A14',      80.0,      109.5], \
	['H6-C2-AS', '1-6-9',    'A15',      80.0,      109.5], \
	['C1-AS-C2', '2-1-6',    'A1',       80.0,      101.2], \
	['C1-AS-O1', '2-1-10',   'A2',       80.0,      108.0], \
	['C1-AS-O2', '2-1-11',   'A3',       80.0,      108.0], \
	['C2-AS-O1', '6-1-10',   'A4',       80.0,      108.0], \
	['C2-AS-O2', '6-1-11',   'A5',       80.0,      108.0], \
	['O1-AS-O2', '10-1-11',  'A6',       80.0,      121.8], \
	['H1-C1-H2', '3-2-4',    'A10',      35.0,      109.50], \
	['H1-C1-H3', '3-2-5',    'A11',      35.0,      109.50], \
	['H2-C1-H3', '4-2-5',    'A12',      35.0,      109.50], \
	['H4-C1-H5', '7-6-8',    'A16',      35.0,      109.50], \
	['H4-C1-H6', '7-6-9',    'A17',      35.0,      109.50], \
	['H5-C1-H6', '8-6-9',    'A18',      35.0,      109.50], \
	]
	TotAngleE=0
	for i in Angles:
		atom=i[1].split('-')
		atom=[int(x) for x in atom]
		r=[coords[atom[0]][0]-coords[atom[1]][0], \
		coords[atom[0]][1]-coords[atom[1]][1], \
		coords[atom[0]][2]-coords[atom[1]][2]]
		s=[coords[atom[2]][0]-coords[atom[1]][0], \
		coords[atom[2]][1]-coords[atom[1]][1], \
		coords[atom[2]][2]-coords[atom[1]][2]]
		magnr=math.sqrt(r[0]**2+r[1]**2+r[2]**2)
		magns=math.sqrt(s[0]**2+s[1]**2+s[2]**2)
		dotpr=(r[0]*s[0])+(r[1]*s[1])+(r[2]*s[2])
		angle= math.acos((dotpr/(magnr*magns)))
		anglediff= (angle-(i[4]*math.pi/180.0))
		k=i[3]
		angleE=k*anglediff**2
		TotAngleE=TotAngleE+angleE
	return TotAngleE

#Calculate the total non-bonded 1-4 interactions energy (VderWaals and electrostatics). 
def Calc14Energy(coords,epsilon, sigma, charge, attypes):
	###########
	#  1-4    #  rmin=sigma1+sigma2; epsilon=sqrt(e1*e2); epsilon[(Rmin/d)^12-2(Rmin/d)^6]
	#         #  1-4's are scaled 5/6 for electrostatic and 1/2 for vdW
	###########
	OneFours=[ \
	['H1-O1', 3, 10], \
	['H1-O2', 3, 11], \
	['H1-C2', 3, 6], \
	['H2-O1', 4, 10], \
	['H2-O2', 4, 11], \
	['H2-C2', 4, 6], \
	['H3-O1', 5, 10], \
	['H3-O2', 5, 11], \
	['H3-C2', 5, 6], \
	['H4-O1', 7, 10], \
	['H4-O2', 7, 11], \
	['H4-C1', 7, 2], \
	['H5-O1', 8, 10], \
	['H5-O2', 8, 11], \
	['H5-C1', 8, 2], \
	['H6-O1', 9, 10], \
	['H6-O2', 9, 11], \
	['H6-C1', 9, 2], \
	]
	Tot14E=0
	for i in OneFours:
		atom=[i[1],i[2]]
		r=[coords[atom[0]][0]-coords[atom[1]][0], \
		coords[atom[0]][1]-coords[atom[1]][1], \
		coords[atom[0]][2]-coords[atom[1]][2]]
		magnr=math.sqrt(r[0]**2+r[1]**2+r[2]**2)
		
		atom1=attypes[i[1]]
		atom2=attypes[i[2]]
		rmin=sigma[atom1]+sigma[atom2]
		e=math.sqrt(epsilon[atom1]*epsilon[atom2])
		qq=charge[atom1]*charge[atom2]
		e14E=(0.5*(e*(((rmin/magnr)**12.0)-2.0*((rmin/magnr)**6.0))))+((5.0/6.0)*((qq/magnr)*332.0522))
		Tot14E=Tot14E+e14E
	return Tot14E

#Calculates the total non-bonded energy (van der waals and electrostatic)
def CalcNonBondEnergy(coords,epsilon, sigma, charge, attypes):
	############
	#  NonBond #  rmin=sigma1+sigma2; epsilon=sqrt(e1*e2); epsilon[(Rmin/d)^12-2(Rmin/d)^6]
	#          #  
	############
	NonBond=[ \
	['H1-H4',  3, 7], \
	['H1-H5',  3, 8], \
	['H1-H6',  3, 9], \
	['H2-H4',  4, 7], \
	['H2-H5',  4, 8], \
	['H2-H6',  4, 9], \
	['H3-H4',  5, 7], \
	['H3-H5',  5, 8], \
	['H3-H6',  5, 9], \
	]
	TotNonBondE=0
	for i in NonBond:
		atom=[i[1],i[2]]
		r=[coords[atom[0]][0]-coords[atom[1]][0], \
		coords[atom[0]][1]-coords[atom[1]][1], \
		coords[atom[0]][2]-coords[atom[1]][2]]
		magnr=math.sqrt(r[0]**2+r[1]**2+r[2]**2)
		atom1=attypes[i[1]]
		atom2=attypes[i[2]]
		rmin=sigma[atom1]+sigma[atom2]
		e=math.sqrt(epsilon[atom1]*epsilon[atom2])
		qq=charge[atom1]*charge[atom2]
		NonBondE=(e*(((rmin/magnr)**12.0)-2.0*((rmin/magnr)**6.0)))+((qq/magnr)*332.0522)
		TotNonBondE=TotNonBondE+NonBondE
	return TotNonBondE

#Creates a row of the A matrix (each column is an angle to be fit. Each element is the cos(3*theta) of that angle at that position.
def MakeArow(coords,pos):
	#makes a row for the A matrix from each conformation. There are 18 dihedrals in cacodylate:
	Dih=[ \
	['D1', 6, 1, 2, 3], \
	['D2', 6, 1, 2, 4], \
	['D3', 6, 1, 2, 5], \
	['D4', 10, 1, 2, 3], \
	['D5', 10, 1, 2, 4], \
	['D6', 10, 1, 2, 5], \
	['D7', 11, 1, 2, 3], \
	['D8', 11, 1, 2, 4], \
	['D9', 11, 1, 2, 5], \
	['D10', 2, 1, 6, 7], \
	['D11', 2, 1, 6, 8], \
	['D12', 2, 1, 6, 9], \
	['D13', 10, 1, 6, 7], \
	['D14', 10, 1, 6, 8], \
	['D15', 10, 1, 6, 9], \
	['D16', 11, 1, 6, 7], \
	['D17', 11, 1, 6, 8], \
	['D18', 11, 1, 6, 9], \
	]
	
	thetas=[]
	arow=[pos]
	engrow=[pos]
	for i in Dih:
		atom=[i[1],i[2],i[3],i[4]]
		ab=[coords[atom[1]][0]-coords[atom[0]][0], coords[atom[1]][1]-coords[atom[0]][1],coords[atom[1]][2]-coords[atom[0]][2]]
		bc=[coords[atom[2]][0]-coords[atom[1]][0], coords[atom[2]][1]-coords[atom[1]][1],coords[atom[2]][2]-coords[atom[1]][2]]
		cd=[coords[atom[3]][0]-coords[atom[2]][0], coords[atom[3]][1]-coords[atom[2]][1],coords[atom[3]][2]-coords[atom[2]][2]]
		CPabcb=cross(ab,bc)
		CPbcdc=cross(bc,cd)
		costheta=vdot(CPabcb, CPbcdc)/sqrt(vdot(CPabcb,CPabcb)*vdot(CPbcdc,CPbcdc))
		scr=cross(CPabcb,CPbcdc)
		if vdot(scr,bc) > 0.0:
			theta=math.acos(costheta)
		else:
			theta=-math.acos(costheta)
		thetas.append(theta)
	for i in thetas:
		arow.append(math.cos(3.0*(i)))
		engrow.append(i*180/math.pi)
	Arow=matrix(arow)
	Engrow=matrix(engrow)
	return Arow, Engrow
	
####Calculate relative B vector (Emin state=0) from total BLYP energies
Babs=genfromtxt('BLYPEN.txt')
B=convertB(Babs)
savetxt('B_relative.txt',B,fmt='%.6f')

####Provide dictonaries
atnames={1:'AS', 2:'C1', 3:'H1', 4:'H2', 5:'H3', 6:'C2', 7:'H4', 8:'H5', 9:'H6', 10:'O1', 11:'O2'}
attypes={1:'AS', 2:'CT', 3:'HC', 4:'HC', 5:'HC', 6:'CT', 7:'HC', 8:'HC', 9:'HC', 10:'O2', 11:'O2'}
sigma={'HC':1.4870, 'CT':1.9080, 'AS':2.3000, 'O2':1.6612}
epsilon={'HC':0.0157, 'CT':0.1094, 'AS':0.2200, 'O2':0.2100}
charge={'HC':0.097778, 'CT':-0.540097, 'AS':1.299626, 'O2':-0.903050}

###Create empty Amatrix
A=zeros((181,19))
Eng=zeros((181,19))
BondE=zeros((181,2))
AngleE=zeros((181,2))
E14E=zeros((181,2))
NonBondE=zeros((181,2))
####Open files
for dire in os.listdir('.'):
	if dire[:9] == 'scan_step':	
		pos=int(dire[9:12])
		k=dire+'/'+dire+'.out'
		#print 'opening   '+k
		
		###Calculate energy component and subtract from B_relative to get dihedral B vector
		TotEnergy=GetTotalGvEnergy(pos,B)
		params, coords, distmat =ReadGvFile(k)
		coordn=namecoords(coords, atnames)
		TotBondE=CalcBondEnergy(coords)
		TotAngleE=CalcAngleEnergy(coords)
		Tot14E=Calc14Energy(coords,epsilon, sigma, charge, attypes)
		TotNonBondE=CalcNonBondEnergy(coords,epsilon, sigma, charge, attypes)
		Penergy=TotBondE+TotAngleE+Tot14E+TotNonBondE
		TotDihE=TotEnergy-Penergy
		B[pos,1]=TotDihE

		BondE[pos,1]=TotBondE
		AngleE[pos,1]=TotAngleE
		E14E[pos,1]=Tot14E
		NonBondE[pos,1]=TotNonBondE
		BondE[:,0]=B[:,0]
		AngleE[:,0]=B[:,0]
		E14E[:,0]=B[:,0]
		NonBondE[:,0]=B[:,0]
		#print "%03d %10.6f\n"% (pos, TotBondE)

		###Calculate A matrix
		Arow,Engrow=MakeArow(coords,pos)
		A[pos,:]=Arow
		Eng[pos,:]=Engrow

		#~ if pos==0:
			#~ print Arow
			#~ print Engrow
		#~ A=vstack((A,Arow))
		#~ Eng=vstack((Eng,Engrow))
		#~ try:
			#~ A=vstack((A,Arow))
		#~ except:
			#~ A=Arow
		#~ if pos == 76:
			#~ for x in params:
				#~ print x, params[x]
			#~ print params['D12']
	else:
		#print dire+'  skipped'
		continue

#~ print coords
#~ print '##########################################'
#~ print coordn
#~ print '##########################################'
#~ print coords[1]
#~ print coords[1][0]

###Save B vector and A matrix
##Need to add as many zeros to bvector as A matrix has constraint rows
m=mean(B[:,1])
for i in range(B.shape[0]):
	B[i,1]=B[i,1]-m
Bzeros=zeros((16,2))
B=vstack((B,Bzeros))
savetxt('B.txt',B[:,1],fmt='%.6f')	



A=A[:,1:] #remove first column which has the conformations
##create constraint rows and add to end of A
x=zeros((16,18))
for i in range(5):
	x[i,0]=1000.0

j=0
for i in [2,3,10,11,12]:
	x[j,i-1]=-1000.0
	j=j+1

j=5
for i in [5,6,7,8,9,13,14,15,16,17,18]:
	x[j,i-1]=-1000.0
	j=j+1

for i in range(11):
	x[i+5,3]=1000.0
A=vstack((A,x))
savetxt('A.txt',A, fmt='%10.6f')

		#~ print TotEnergy
		#~ print TotDihE
		#~ print TotBondE
		#~ print TotAngleE
		#~ print Tot14E
		#~ print TotNonBondE

#like A matrix but has the original values of each dihedral
Eng=Eng[:,1:]
savetxt('Eng.txt',Eng,fmt='%10.6f')


savetxt('BondE_byhand.txt',BondE,fmt='%10.6f')
savetxt('AngleE_byhand.txt',AngleE,fmt='%10.6f')
savetxt('E14E_byhand.txt',E14E,fmt='%10.6f')
savetxt('NonBondE_byhand.txt',NonBondE,fmt='%10.6f')



#~ for i in (BLYPEN[:,0]/2):
	#~ print int(i)

#~ 
#~ yyy={'AS':{'x':5,'y':6,'z':7}}
#~ for key in atnames.keys():
	#~ print atnames[key]+'x'
		#~ 
#print n.split()
#print nn


#~ str = "Line1-abcdef \nLine2-abc \nLine4-abcd";
#~ print str.split( );
#~ print str.split(' ', 1 );

#~ # x[9][27:55]
#~ #for i in x[9]:
#~ #	print i
#~ 
#~ 
#~ print x[9][27:55]
#~ print y[27:55]
#~ 
#~ if x[9][27:55] == y[27:55]:
	#~ print 'hello'
#~ 
#~ if x[9] == y:
	#~ print 'hello'
