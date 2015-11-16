#! /usr/bin/env python

import sander
from chemistry.amber.readparm import AmberParm, Rst7
import numpy as np

pdb ='3stl'
parm = AmberParm('4amber_%s.prmtop' %pdb)  #topo
rst = Rst7.open('4amber_%s.rst7' %pdb)     #box
sander.setup(parm, rst.coordinates, rst.box, sander.pme_input())
ene, frc = sander.energy_forces()
print ene.tot
print max(frc)

import code; code.interact(local=dict(globals(), **locals()))
sander.cleanup()

