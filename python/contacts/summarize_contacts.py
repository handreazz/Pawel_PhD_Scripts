#! /usr/bin/python
import sys
import os
from numpy import *



#======================================================================#
#======================================================================#
############################
###    INTERFACE DATA    ###
############################

class Interface:
  'Interface description includes interacting ASUs, bonds, residues'
  def __init__(self,ASU=[],HB_cryst=[],HB_sim=[],IFACE=[],name='noname'):
    self.ASU=ASU
    self.HB_cryst=HB_cryst
    self.HB_sim=HB_sim
    self.IFACE=IFACE
    self.name=name
#Y
Y=Interface(name='Y')
Y.ASU=[ \
[1,3],[3,1], \
[2,4],[4,2], \
[5,7],[7,5], \
[6,8],[8,6], \
[9,11],[11,9], \
[10,12],[12,10], \
]

Y.HB_cryst=[ \
[':21@NH2',':66@O'], \
[':19@ND2',':81@O'], \
]

Y.HB_sim=[ \
[':19@ND2',':84@O'], \
[':19@OD1',':41@NE2'], \
[':23@OH',':68@NH1'], \
[':21@O',':68@NH1'], \
[':21@O',':68@NH2'], \
]

Y.IFACE=[ \
'2,39,41,43,45,53,66-68,81,84,85', \
'18,19,21-24,27,99,102-104,106,111,116,117,121,124', \
]

#X
X=Interface(name='X')
X.ASU=[ \
[1,5],[5,9],[9,1], \
[2,6],[6,10],[10,2], \
[3,7],[7,11],[11,3], \
[4,8],[8,12],[12,4], \
]

X.HB_cryst=[ \
[':45@O',':77@ND2'], \
[':46@O',':77@ND2'], \
[':37@ND2',':14@O'], \
[':114@NH1',':16@O'], \
[':114@NH2',':18@O'], \
]

X.HB_sim=[ \
[':47@OG1',':75@O'], \
[':47@OG1',':97@NZ'], \
[':47@OG1',':77@ND2'], \
[':113@OD1',':21@NH1'], \
[':114@NH1',':18@O'] \
]

X.IFACE=[ \
'33,34,37,44-47,113,114', \
'14-16,18-21,73-77,96-97', \
]

#Z
Z=Interface(name='Z')
Z.ASU=[ \
[1,2], [2,1], \
[3,4], [4,3], \
[5,6], [6,5], \
[7,8],[8,7], \
[9,10],[10,9], \
[11,12],[12,11], \
]

Z.HB_cryst=[ \
[':100@OG',':128@NH1'], \
[':101@O',':5@NH2'], \
[':73@NH1',':3@O'], \
]

Z.HB_sim=[ \
[':102@N',':126@O'], \
[':97@NZ',':7@OE1'], \
]

Z.IFACE=[ \
'2-7,33,37,38,125-128', \
'20,21,62,71-73,75,97,100-103', \
]

#XZ
XZ=Interface(name='XZ')
XZ.ASU=[ \
[1,6],[2,5], \
[5,10],[6,9], \
[9,2],[10,1], \
[3,8],[7,12], \
[11,4],[4,7], \
[8,11],[12,3], \
]

XZ.HB_cryst=[ \
[':47@O',':1@NZ'], \
[':48@OD2',':14@NH1'], \
[':48@OD2',':14@NH2'], \
]

XZ.HB_sim=[ \
[':52@OD1',':128@NH1'], \
[':52@OD2',':128@NH1'], \
[':52@OD1',':128@NH2'], \
[':52@OD2',':128@NH2'], \
[':106@O',':128@NH1'], \
[':106@O',':128@NH2'], \
]

XZ.IFACE=[ \
'47,48,61,62,109,112,113', \
'7,14,128,129', \
]

#XY
XY=Interface(name='XY')
XY.ASU=[ \
[1,7],[2,8], \
[5,11],[6,12], \
[9,3],[10,4], \
[3,5],[4,6], \
[7,9],[8,10], \
[11,1],[12,2], \
]

XY.HB_cryst=[ \
[':113@O',':81@OG'], \
[':116@NZ',':77@OD1'], \
]

XY.HB_sim=[ \
[':119@N',':87@OD1'], \
[':119@N',':87@OD2'], \
]

XY.IFACE=[ \
'112-114,116-117', \
'65,74,77-79,81,82,85,87,89,90,93', \
]

#YZ
YZ=Interface(name='YZ')
YZ.ASU=[ \
[2,3],[3,2], \
[1,4],[4,1], \
[6,7],[7,6], \
[5,8],[8,5], \
[10,11],[11,10], \
[9,12],[12,9], \
]

YZ.HB_cryst=[]
YZ.HB_sim=[]

YZ.IFACE=[ \
'67-71', \
'119,121,125-126', \
]
interfaces=[Y,Z,X,XZ,XY,YZ]

#======================================================================#
#======================================================================#
############################
###        FUNCTIONS     ###
############################

def BondSummary(iface,bond,cutoff,crystORsym):
  res1=int(bond[0].split(':')[1].split('@')[0])
  res2=int(bond[1].split(':')[1].split('@')[0])
  atm1=bond[0].split(':')[1].split('@')[1]
  atm2=bond[1].split(':')[1].split('@')[1]
  # container with percent that bond is present
  #       first field - if present in crystal
  #       second field - percent over all ASU, all trajectory
  #       third+ fields - percent for each ASU, all trajectory
  summary=[0]*14
  total_all_asus=0
  for pair_index,pair in enumerate(iface.ASU):    
    ASU1=pair[0]
    ASU2=pair[1]
    res1_c=res1+Nres*(ASU1-1)
    res2_c=res2+Nres*(ASU2-1)
    mask1=':%d@%s' %(res1_c,atm1)
    mask2=':%d@%s' %(res2_c,atm2)
    file='output/%s_%dASU%d_%s%s_%s' %(iface.name,ASU1,ASU2,mask1,mask2,crystORsym)
    data=genfromtxt(file)
    total_this_asu=float(sum(data[:,1] < cutoff))
    summary[ASU1+1]=(total_this_asu/data.shape[0])*100
    total_all_asus += total_this_asu
  summary[1] = total_all_asus/(data.shape[0]*(pair_index+1)) * 100  
  summary[0] = data[0,1] <cutoff
  return summary


def BondName(bond):
  return "%s--%s" %(bond[0],bond[1])



def PrintBond(f, ifacename, bond_name, bond_summary):
  f.write("%4s %20s  %2d      %2d   " 
            %(ifacename,bond_name, bond_summary[0], bond_summary[1]))
  for i in range(len(bond_summary)-2):
    f.write("%2d   " %bond_summary[i+2])
  f.write("\n") 

#======================================================================#
#======================================================================#
############################
###        MAIN          ###
############################

interfaces=[Y,Z,X,XZ,XY,YZ]
#~ interfaces=[X]
Nres=139
cutoff=3.9
ofile="contact_summary.txt"
n_asu=12

f=open(ofile,'w')
f.write("Iface   Bondname           Cryst   Total")
for i in range(n_asu):
  f.write("%2d   " %(i+1))
f.write("\n")
f.write("-"*42+"-"*n_asu*5+"\n")

for iface in interfaces:
  summaries=[]
 
  for bond in iface.HB_cryst:
    crystORsym="cryst"
    bond_name = BondName(bond)
    bond_summary = BondSummary(iface,bond,cutoff,crystORsym)
    summaries.append([bond_summary, bond_name])
 
  for bond in iface.HB_sim:
    crystORsym="sim"
    bond_name = BondName(bond)
    bond_summary = BondSummary(iface,bond,cutoff,crystORsym)
    summaries.append([bond_summary, bond_name])
  
  summaries.sort(key=lambda x: (-x[0][0], -x[0][1]) )
  for bond in summaries:
    PrintBond(f, iface.name, bond[1], bond[0])
  f.write("\n")
f.close()

