#! /usr/bin/python
import ReadAmberFiles as raf
from numpy import *
import sys

#######################################################################	
# Generate REMARK 290 SMTRY CARDS given space group and unit cell.    #
# Arguments:                                                          #
#     box:  6x1 numpy array of box parameters                         #
#     symops: symmetry operation matrices as found in space_group.cif #
#             If this file is not available, operations are in        #
#             CCP4HOME/lib/data/symop.lib and need to get turned into #
#             numbers.                                                #
# Returns:                                                            #
#     prints SMTRY records to stty                                    #
#######################################################################

# Fill in box and symops below.
# Example: PDB:2p7e ; Spacegroup: P 61 2 2
box = array( (66.81, 66.81, 170.79, 90., 90., 120.) )
symops=\
'''\
'P 61 2 2'        1    1  0  0    0  1  0    0  0  1    0  0    0  0    0  0
'P 61 2 2'        2    0 -1  0    1 -1  0    0  0  1    0  0    0  0    1  3
'P 61 2 2'        3   -1  1  0   -1  0  0    0  0  1    0  0    0  0    2  3
'P 61 2 2'        4   -1  0  0    0 -1  0    0  0  1    0  0    0  0    1  2
'P 61 2 2'        5    0  1  0   -1  1  0    0  0  1    0  0    0  0    5  6
'P 61 2 2'        6    1 -1  0    1  0  0    0  0  1    0  0    0  0    1  6
'P 61 2 2'        7    0  1  0    1  0  0    0  0 -1    0  0    0  0    1  3
'P 61 2 2'        8    1 -1  0    0 -1  0    0  0 -1    0  0    0  0    0  0
'P 61 2 2'        9   -1  0  0   -1  1  0    0  0 -1    0  0    0  0    2  3
'P 61 2 2'       10    0 -1  0   -1  0  0    0  0 -1    0  0    0  0    5  6
'P 61 2 2'       11   -1  1  0    0  1  0    0  0 -1    0  0    0  0    1  2
'P 61 2 2'       12    1  0  0    1 -1  0    0  0 -1    0  0    0  0    1  6 '''

#========================================================================#
#========================================================================#


def compute_ortho(box):
#######################################################################
# Calculate deorthogonalization matrix u and orthogonalization matrix #
# 	invu. Invu is used to take fractional coordinates into cartesian  #
#	space and u is used to take cartesian coordinates into fractional   #
#	space.                                                              #
# Arguments:                                                          #
#     box: 1x6 array of box vectors [a,b,c,alpha,beta,gamma]          #
#          This is usually taken from rst7 file class, Get_Box routine#
#          Angles must be in degrees.								                  #
# Returns:                                                            #
#     u: 3x3 array                                                    #
#	  invu: 3x3 array	                                                  #
#######################################################################
  box=box.astype(float)
  box[3:6]=radians(box[3:6])
  a,b,c,alpha,beta,gamma=box[0],box[1],box[2],box[3],box[4],box[5]
  volume=a*b*c*sqrt(1-cos(alpha)**2-cos(beta)**2-cos(gamma)**2+2*cos(alpha)*cos(beta)*cos(gamma))
  invu=zeros((3,3))
  invu[0,0]=a
  invu[0,1]=b*cos(gamma)
  invu[0,2]=c*cos(beta)
  invu[1,1]=b*sin(gamma)
  invu[1,2]=c*(cos(alpha)-(cos(beta)*cos(gamma)))/sin(gamma)
  invu[2,2]=volume/(a*b*sin(gamma))
  u=linalg.inv(invu)
  return u, invu

def process_symops(symops):
  numops=len(symops.splitlines())
  Rf=zeros((numops,3,3))
  Tf=zeros((numops,3))
  op=0
  for line in symops.splitlines():
    line=line.split('\'')[-1].split()
    for i in range(3):
      for j in range(3):
        Rf[op][i][j]=line[i*3+j+1]
      try:
        Tf[op][i]=float(line[((i*2)-1+11)])/float(line[((i*2)+11)])
      except ZeroDivisionError:
        Tf[op][i]=0.0
    op+=1
  return numops, Rf, Tf

def print_SMTRY(numops, Rf, Tf):
  Tc=zeros(shape(Tf))
  for i in range(numops):
    Tc[i]=dot(invu,Tf[i]).astype(float32)
  Rc=zeros(shape(Rf))
  for i in range(numops):
    Rc[i]=dot(dot(invu,Rf[i]),u)
  for op in range(numops):
    for i in range(3):
      print("REMARK 290   SMTRY%d%4d%10.6f%10.6f%10.6f%15.5f" %(i+1,op+1,Rc[op][i][0], Rc[op][i][1], Rc[op][i][2], Tc[op][i]))

if __name__ ==  "__main__":
  u,invu = compute_ortho(box)
  numops, Rf, Tf = process_symops(symops)
  print_SMTRY(numops, Rf, Tf)


