#! /usr/bin/python
import sys
import os
from numpy import *
from ReadAmberFiles import *
from Scientific.IO import NetCDF as Net

file1='UC.rst7'
file2='str2.rst7'
topo='UC.prmtop'

RST7=rst7(file1)
str1=RST7.Get_Coords()
RST7=rst7(file2)
str2=RST7.Get_Coords()
PRM=prmtop(topo)
masses=PRM.Get_Masses()

str3=KabschAlign(str1, str2,masses)
rmsd=KabschRMSD(str1,str2,masses)

print RMSD(str1,str3)
print RMSD(str1,str3,masses)
print rmsd 
printmdcrd(str3,' ', 'new.mdcrd','by pawel')
