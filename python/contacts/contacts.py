#! /usr/bin/python
import sys
import os
from numpy import *


############################################################################
# For each given interface and defined ASU's that form that interface,     #
# crystal and simulation bonds that form along that interface and residues #
# that make up that interface (data from PISA), calculate change in bond   #
# distances, center of mass distances of ASU's and of interface residues   #
# during the course of the simulation trajectory.                          #
############################################################################


##################################
###   DEFINE INTERFACE CLASS   ###
##################################
class Interface:
  'Interface description includes interacting ASUs, bonds, residues'
  def __init__(self,ASU=[],HB_cryst=[],HB_sim=[],IFACE=[],name='noname'):
    self.ASU=ASU
    self.HB_cryst=HB_cryst
    self.HB_sim=HB_sim
    self.IFACE=IFACE
    self.name=name
  def CalcBondsCryst(self):
    for pair in self.ASU:
      ASU1=pair[0]
      ASU2=pair[1]
      for bond in self.HB_cryst:
        res1=int(bond[0].split(':')[1].split('@')[0])
        res2=int(bond[1].split(':')[1].split('@')[0])
        atm1=bond[0].split(':')[1].split('@')[1]
        atm2=bond[1].split(':')[1].split('@')[1]
        res1=res1+Nres*(ASU1-1)
        res2=res2+Nres*(ASU2-1)
        mask1=':%d@%s' %(res1,atm1)
        mask2=':%d@%s' %(res2,atm2)
        f=open('ptraj_dist','w')
        f.write('trajin /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_centonpdb_nowat.rst7\n')
        f.write('trajin ../fit.nc\n')
        f.write('distance name %s %s out output/%s_%dASU%d_%s%s_cryst\n' %(mask1,mask2,self.name,ASU1,ASU2,mask1,mask2))
        f.close()
        os.system('cpptraj /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_nowat.prmtop <ptraj_dist')
  def CalcBondsSim(self):
    for pair in self.ASU:
      ASU1=pair[0]
      ASU2=pair[1]      
      for bond in self.HB_sim:
        res1=int(bond[0].split(':')[1].split('@')[0])
        res2=int(bond[1].split(':')[1].split('@')[0])
        atm1=bond[0].split(':')[1].split('@')[1]
        atm2=bond[1].split(':')[1].split('@')[1]
        res1=res1+Nres*(ASU1-1)
        res2=res2+Nres*(ASU2-1)
        mask1=':%d@%s' %(res1,atm1)
        mask2=':%d@%s' %(res2,atm2)
        f=open('ptraj_dist','w')
        f.write('trajin /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_centonpdb_nowat.rst7\n')        
        f.write('trajin ../fit.nc\n')
        f.write('distance name %s %s out output/%s_%dASU%d_%s%s_sim\n' %(mask1,mask2,self.name,ASU1,ASU2,mask1,mask2))
        f.close()
        os.system('cpptraj /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_nowat.prmtop <ptraj_dist')
  def CalcAsuComDist(self):
    for pair in self.ASU:
      ASU1=pair[0]
      ASU2=pair[1]
      ASU1_init= 1+Nres*(ASU1-1)
      ASU1_end= Nres*ASU1
      ASU2_init= 1+Nres*(ASU2-1)
      ASU2_end= Nres*ASU2
      mask1=':%d-%d' %(ASU1_init,ASU1_end)
      mask2=':%d-%d' %(ASU2_init,ASU2_end)
      f=open('ptraj_dist','w')
      f.write('trajin /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_centonpdb_nowat.rst7\n')
      f.write('trajin ../fit.nc\n')
      try:
        if pair[2] == 'image':
          f.write('distance name %s %s out output/%s_%dASU%d_com\n' %(mask1,mask2,self.name,ASU1,ASU2))
      except IndexError:
        f.write('distance name %s %s out output/%s_%dASU%d_com noimage\n' %(mask1,mask2,self.name,ASU1,ASU2))
      f.close()
      os.system('cpptraj /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_nowat.prmtop <ptraj_dist >tmp.dat')  
  def CalcIfaceComDist(self):
    for pair in self.ASU:
      ASU1=pair[0]
      ASU2=pair[1]
      mask1=[]
      for residue in self.IFACE[0].split(','):
        if '-' in residue:
          start_res=int(residue.split('-')[0])+Nres*(ASU1-1)
          end_res=int(residue.split('-')[1])+Nres*(ASU1-1)
          residue=str(start_res)+'-'+str(end_res)
          mask1.append(residue) 
        else:
          residue=str(int(residue)+Nres*(ASU1-1))
          mask1.append(residue)
      mask1=':'+','.join(mask1)
      mask2=[]
      for residue in self.IFACE[1].split(','):
        if '-' in residue:
          start_res=int(residue.split('-')[0])+Nres*(ASU2-1)
          end_res=int(residue.split('-')[1])+Nres*(ASU2-1)
          residue=str(start_res)+'-'+str(end_res)
          mask2.append(residue) 
        else:
          residue=str(int(residue)+Nres*(ASU2-1))
          mask2.append(residue)
      mask2=':'+','.join(mask2)
      f=open('ptraj_dist','w')
      f.write('trajin /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_centonpdb_nowat.rst7\n')
      f.write('trajin ../fit.nc\n')
      f.write('distance name %s %s out output/%s_%dASU%d_IfaceCom\n' %(mask1,mask2,self.name,ASU1,ASU2))
      f.close()
      os.system('cpptraj /home/pjanowsk/c/Case/4lzt/RunSi/4lztSc_nowat.prmtop <ptraj_dist') 

########################################################################
#######################
### SET ARGUMENTS   ###
#######################

#Y
Y=Interface(name='Y')
Y.ASU=[ \
[1,3],[3,1,'image'], \
[2,4],[4,2,'image'], \
[5,7],[7,5,'image'], \
[6,8],[8,6,'image'], \
[9,11],[11,9,'image'], \
[10,12],[12,10,'image'], \
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
[1,5],[5,9],[9,1,'image'], \
[2,6],[6,10],[10,2,'image'], \
[3,7],[7,11],[11,3,'image'], \
[4,8],[8,12],[12,4,'image'], \
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
[1,2], [2,1,'image'], \
[3,4], [4,3,'image'], \
[5,6], [6,5,'image'], \
[7,8],[8,7,'image'], \
[9,10],[10,9,'image'], \
[11,12],[12,11,'image'], \
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
[1,6],[2,5,'image'], \
[5,10],[6,9,'image'], \
[9,2,'image'],[10,1,'image'], \
[3,8],[7,12,'image'], \
[11,4,'image'],[4,7,'image'], \
[8,11,'image'],[12,3,'image'], \
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
[9,3,'image'],[10,4,'image'], \
[3,5,'image'],[4,6,'image'], \
[7,9,'image'],[8,10,'image'], \
[11,1,'image'],[12,2,'image'], \
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
[2,3],[3,2,'image'], \
[1,4,'image'],[4,1,'image'], \
[6,7],[7,6,'image'], \
[5,8,'image'],[8,5,'image'], \
[10,11],[11,10,'image'], \
[9,12,'image'],[12,9,'image'], \
]

YZ.HB_cryst=[]
YZ.HB_sim=[]

YZ.IFACE=[ \
'67-71', \
'119,121,125-126', \
]

Nres=139
interfaces=[Y,Z,X,XZ,XY,YZ]
#~ interfaces=[X]
########################################################################
############################
###        MAIN          ###
############################
os.system('mkdir -p output')
for i in interfaces:
  i.CalcBondsCryst()
  #~ i.CalcBondsSim()
  i.CalcAsuComDist()
  #~ i.CalcIfaceComDist()
#~ Z.CalcBondsSim()
#~ Z.CalcBondsCryst()
#~ Z.CalcIfaceComDist()
#~ Z.CalcAsuComDist()
#~ X.CalcBondsSim()
