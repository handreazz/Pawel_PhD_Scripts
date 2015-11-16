#! /usr/bin/env python

import sander
from chemistry.amber.readparm import AmberParm, Rst7
from chemistry.structure import Structure, read_PDB, write_PDB
import numpy as np


parm = AmberParm('4amber_1cby.prmtop')
pdb = read_PDB('new.pdb')
rst = Rst7.open('4amber_1cby.rst7')
xyz = pdb.pdbxyz[0]
sander.setup(parm,xyz, rst.box, sander.pme_input())

sander.set_positions(xyz)
ene, frc = sander.energy_forces()

#~ import code; code.interact(local=dict(globals(), **locals()))
sander.cleanup()

