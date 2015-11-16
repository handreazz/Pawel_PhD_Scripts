#! /usr/bin/env python

from numpy import sqrt
import sys, os

cc = float(sys.argv[1]) #correlation coefficient
n  = int(sys.argv[2]) # number of data points

print (1 - cc*cc)/sqrt(n-1)
