from __future__ import division
from scitbx.array_family import flex
from math import acos, pi

def dotproduct():
  a=[3,-4,1]
  b=[0,5,2]
  a1=flex.double(a)
  b1=flex.double(b)
  angle = acos(a1.dot(b1)/(a1.norm()*b1.norm()))*180/pi
  return angle

def lawcosines():
  a=[3,-4,1]
  b=[0,5,2]
  a1=flex.double(a)
  b1=flex.double(b)
  c1=a1-b1
  angle = acos((a1.norm()**2+b1.norm()**2-c1.norm()**2)/(2*a1.norm()*b1.norm()))*180/pi
  return angle


#to test run in terminal
#  phenix.python -mtimeit -s'import brmsd' 'brmsd.lawcosines()'
#  phenix.python -mtimeit -s'import brmsd' 'brmsd.dotproduct()'