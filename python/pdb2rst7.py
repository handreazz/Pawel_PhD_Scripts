#! /usr/bin/python
import ReadAmberFiles as raf

apdb=raf.pdb('vAla3_minimized.pdb')
box=apdb.Get_Box()
coords=apdb.Get_Coords()
natoms=natoms= len(apdb.ATOMlines)
raf.printrst7(coords, box, natoms, 'vAla3_minimized.rst7', comment='rst7 written by pawel')



