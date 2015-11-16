#! /usr/bin/python
import ReadAmberFiles as raf
from numpy import *
import sys

#######################################################################	
# Generate REMARK 290 SMTRY CARDS given space group and unit cell.    #
# Arguments:                                                          #
#     pdbfile:  name of pdbfile with CRYST1 record (eg. output from   #
#               Phenix)                                               #
#     symops: symmetry operation matrices as found in space_group.cif #
#             file. (/bin/prog-vari/auto-cryst-data/space_group.cif)  #
#                   (~/c/scripts/crystallography/)                    #
#             If this file is not available, operations are in        #
#             CCP4HOME/lib/data/symop.lib and need to get turned into #
#             numbers.                                                #
# Returns:                                                            #
#     prints SMTRY records to stty                                    #
#######################################################################


#2p7e: P 61 2 2
pdbfile='/net/casegroup2/u2/pjanowsk/Phenix/1cby/4phenix_1cby_minall.pdb'
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

#========================================================================

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

pdbf=raf.pdb(pdbfile)
box=pdbf.Get_Box()
print box, type(box)
u,invu=raf.CompXfrm(box)


print "================================"
Tc=zeros(shape(Tf))
for i in range(numops):
	Tc[i]=dot(invu,Tf[i]).astype(float32)
#~ print Tc
print "================================"

Rc=zeros(shape(Rf))
for i in range(numops):
	Rc[i]=dot(dot(invu,Rf[i]),u)
#~ print Rc
print "================================"

import code; code.interact(local=dict(globals(), **locals()))

for op in range(numops):
	for i in range(3):
		print("REMARK 290   SMTRY%d%4d%10.6f%10.6f%10.6f%15.5f" %(i+1,op+1,Rc[op][i][0], Rc[op][i][1], Rc[op][i][2], Tc[op][i]))

