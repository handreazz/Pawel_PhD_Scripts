#! /usr/bin/env python

import sander
from parmed.amber.readparm import AmberParm, Rst7
import numpy as np
import os, sys
import pickle


base = '1nie'
# parm = AmberParm('4amber_%s.prmtop' %base)  #topo
rst = Rst7.open('4amber_%s.rst7' %base)     #box
coords1 = rst.coordinates
coords2 = np.around( np.array(pickle.load(open('tmp2','rb') ) ), 3) #2nd coordinate set
print coords1, coords1.shape
print coords2, coords2.shape

sander.setup('4amber_%s.prmtop' %base, rst.coordinates, rst.box, sander.pme_input())
ene, frc = sander.energy_forces()
print frc[0]

sander.set_positions(coords1)
ene, frc = sander.energy_forces()
print frc[0]

sander.set_positions(coords2)
ene, frc = sander.energy_forces()
print frc[0]
print max(frc)
print ene.tot, ene.elec, ene.vdw
# import code; code.interact(local=dict(globals(), **locals()))
import boost.python

sander.set_positions(rst.coordinates)
ene, frc = sander.energy_forces()
print frc[0]

sander.set_positions(coords1)
ene, frc = sander.energy_forces()
print frc[0]

sander.set_positions(coords2)
ene, frc = sander.energy_forces()
print frc[0]
print max(frc)
print ene.tot, ene.elec, ene.vdw

sander.cleanup()
