#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib.pyplot as plt

fig=plt.figure()
data=genfromtxt('waterdist/new2.dat')
plt.plot(data[:,0],data[:,1])
plt.plot(data[:,0],data[:,2])
plt.suptitle('comparison of distance by vmd(green) and ptraj (blue)')
plt.show()
