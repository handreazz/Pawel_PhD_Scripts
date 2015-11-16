from numpy import *
import sys

cmd.delete("all")
cmd.load( "../4lzt_quasi.pdb", "full")
cmd.create("anew", "full", 1, 1)
print "First 3 shifts: ", nm[0:3], "\n"


cmd.alter_state(1,"anew" , "x,y,z = x+nm[(ID-1)*3], y+nm[(ID-1)*3+1], z+nm[(ID-1)*3+2]")

xyz1=[]
cmd.iterate_state(1, 'full & id 5', 'xyz1.append([x,y,z])')
xyz2=[]
cmd.iterate_state(1, 'anew & id 1', 'xyz2.append([x,y,z])')
print "Coords of full id 5:", array(xyz1)
print "Coords of anew id 1:",  array(xyz2)
print "Shift between full id5 and anew id1:", array(xyz1)-array(xyz2), "\n"

xyz1=[]
cmd.iterate_state(1, 'full & resid 1 & name ca ', 'xyz1.append([x,y,z])')
xyz2=[]
cmd.iterate_state(1, 'anew & resid 1 & name ca ', 'xyz2.append([x,y,z])')
print "Coords of full resid1 name ca: ", array(xyz1)
print "Coords of full resid1 name ca: ", array(xyz2)
print "Shift between full id5 and anew id1: ", array(xyz1)-array(xyz2)
print "\n"
