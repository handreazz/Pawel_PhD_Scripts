#! /usr/bin/python
import sys
import os
from numpy import *

####
#Return residue number in a differen ASU.
#Arguments:
#	chain - letter name of chain corresponding to target ASU (assumes ASU chains increase alphabetically)
#	residue - residue number in 1st ASU (ie in chain A)
####

### SET ARGUMENTS ###
Nres=139 # no of residues per ASU

########################################################################

labels=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a']



pos=labels.index(sys.argv[1])
res=int(sys.argv[2])-pos*Nres
print res
