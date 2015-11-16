#! /usr/bin/env python
import ReadAmberFiles as raf

iprmtop=raf.prmtop('/net/casegroup2/u2/pjanowsk/Case/4lzt/4lzt_ff12SB/4lztSh_new.prmtop')
masses=iprmtop.Get_Masses()
totalmass=sum(masses)
irst7=raf.rst7('/net/casegroup2/u2/pjanowsk/Case/4lzt/4lzt_ff12SB/4lztSh.rst7')
box=irst7.Get_Box()
volume=raf.Get_volume(box)
density= totalmass/volume*10/6.022
print "density: %8.3f g/cm^3" %density
