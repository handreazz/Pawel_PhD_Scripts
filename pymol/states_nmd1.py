from numpy import *
import sys

set_printoptions(precision=4, linewidth=150)
cmd.delete( all)
cmd.load( "../4lzt_quasi.pdb", "full")
cmd.create("anew", "full", 1, 1)
print cmd.count_atoms("full")
print len(nm)
cmd.alter_state(1,"anew" , "x,y,z = x+nm[(ID-1)*3], y+nm[(ID-1)*3+1], z+nm[(ID-1)*3+2]")
print nm[0:2]
xyz1=[]
cmd.iterate_state(1, 'full & resid 1 & name n', 'xyz1.append([x,y,z])')
xyz2=[]
cmd.iterate_state(1, 'anew & resid 1 & name n', 'xyz2.append([x,y,z])')
print xyz1
print xyz2
print array(xyz1)-array(xyz2)
print "\n"

xyz1=[]
cmd.iterate_state(1, 'full & resid 1 & name ca', 'xyz1.append([x,y,z])')
xyz2=[]
cmd.iterate_state(1, 'anew & resid 1 & name ca', 'xyz2.append([x,y,z])')
print xyz1
print xyz2
print array(xyz1)-array(xyz2)
print "\n"

xyz1=[]
cmd.iterate_state(1, 'full & id 1', 'xyz1.append([x,y,z])')
xyz2=[]
cmd.iterate_state(1, 'anew & id 1', 'xyz2.append([x,y,z])')
print xyz1
print xyz2
print array(xyz1)-array(xyz2)
print "\n"

#~ sys.exit()



#~ iterate_state 1, full & id 1, print x, y
#~ iterate_state 1, anew & id 1, print x, y

#~ what=iterate_state 1, full & resid 1 & name ca, print x, y, z
#~ print what
#~ iterate_state 1, anew & resid 1 & name ca, print x, y, z

#~ iterate_state 1, full & resid 1 & name n, print x, y, id
#~ iterate_state 1, anew & resid 1 & name n, print x, y, id



#~ nnm=nm[0:1961]
#~ print len(nnm)
#~ cmd.create("anew", "full", 1, 2)
#~ cmd.alter_state(2,"anew" , "x,y,z = x+nnm[(ID-1)], y+nnm[(ID-1)], z+nnm[(ID-1)]")
#~ 
#~ print nmm[0:6]
#~ iterate_state 1, full & id 1, print x,y
#~ iterate_state 2, anew & id 1 & name ca, print x,y
#~ 
#~ xyz1=[]
#~ cmd.iterate_state(1, 'full & resid 1 & name n', 'xyz1.append([x,y,z])')
#~ cmd.iterate_state(1, 'full & resid 1 & name ca', 'xyz1.append([x,y,z])')
#~ xyz2=[]
#~ cmd.iterate_state(1, 'anew & resid 1 & name n', 'xyz2.append([x,y,z])')
#~ cmd.iterate_state(1, 'anew & resid 1 & name ca', 'xyz2.append([x,y,z])')
#~ 
#~ for i,j in zip(xyz1, xyz2): print i-j
