#! /usr/bin/python
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import argparse
import sys

#======================================================================#
#                                                                      #
# Quick command line plot.                                             #
# Eg. usage:                                                           #
#           ./plotpy.py bfactors.dat -sh 1 -y 2,3,4                    #
#                                                                      #
#======================================================================#

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Name of file with data")
parser.add_argument("-x", help="Column with x-axis data. Default is column 0.",default="0")
parser.add_argument("-y", help="Column(s) with y-axis data separated by commas (eg. 1,3,4). Default is column 1.",default="1")
parser.add_argument("-sh", help='Header lines to skip when importing data', default="0")
parser.add_argument('-no_x', help='Set this flag if there is no x column in the data file.', action='store_true', default=False)
args = parser.parse_args()


def filter2list(str):
	residues=[ i.split('-') for i in str.split(',')]
	residues=[ [int(i) for i in j] for j in residues]
	tmp=[]
	for i in residues:
		if len(i) == 1:
			tmp.append(i[0])
		if len(i) == 2:
			tmp.extend(range(i[0],i[1]+1))
	return tmp
columns=filter2list(args.y)
x=int(args.x)
data=genfromtxt(args.file,skip_header=int(args.sh))




plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
plt.rc('axes',linewidth=3)
plt.rc('legend', fontsize=20) 
plt.rc('lines', markeredgewidth=2)
plt.rc('xtick.minor',size=5)
plt.rc('xtick.major',size=10)
plt.rc('lines', linewidth=3) 



fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
#exception for single column data files
if shape(shape(data))[0]==1:
	columns=[0]
	ax.plot(data)
	plt.show()
	sys.exit()

if args.no_x:
	for column in columns:
		ax.plot(data[:,column])
	plt.show()
	sys.exit()	
	
for column in columns:
	ax.plot(data[:,x],data[:,column])
#~ ax.grid()
plt.show()
