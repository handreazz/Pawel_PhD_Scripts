#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

#plots the revsym_com_shifts.dat and split_com_shifts.dat. Set variables.

#======================================================================#
# SET VARIABLES
ix=3
iy=2
iz=2
n_asu=1
#======================================================================#

n_uc=ix*iy*iz
revsym=genfromtxt('revsym_com_shifts.dat')
split=genfromtxt('split_com_shifts.dat')


#####################################
# GENERAL PLOT SETTINGS             #
#####################################
from matplotlib.font_manager import fontManager, FontProperties
font=FontProperties(size=10)
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=5, size=5, width=3)
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20)
colors=['#F86606',\
 '#CC0000', \
 '#F3EF02', \
 '#5DF304', \
 '#4E9A06', \
 '#C4A000', \
 '#729FCF', \
 '#0618F4', \
 '#06EFF4', \
 '#A406F4', \
 '#F4069D', \
 '#936F70']  

fig=plt.figure(figsize=(16, 12))
fig.suptitle('Average center of mass of each ASU relative to experiment', fontsize=16)
fig.subplots_adjust(wspace=.20,right=.99, left=.05,top=.93, bottom=.05, hspace=.35)

ax = fig.add_subplot(2,3,1)
ax.scatter(split[:,0], split[:,1])
plt.xlabel('x')
plt.ylabel('y',labelpad=0)
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)


ax = fig.add_subplot(2,3,2)
ax.scatter(split[:,0], split[:,2])
plt.xlabel('x')
plt.ylabel('z',labelpad=0)
plt.title('split')
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

ax = fig.add_subplot(2,3,3)
ax.scatter(split[:,1], split[:,2])
plt.xlabel('y')
plt.ylabel('z',labelpad=0)
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

ax = fig.add_subplot(2,3,4)
ax.scatter(revsym[:,0], revsym[:,1])
plt.xlabel('x')
plt.ylabel('y',labelpad=0)
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

ax = fig.add_subplot(2,3,5)
ax.scatter(revsym[:,0], revsym[:,2])
plt.xlabel('x')
plt.ylabel('z',labelpad=0)
plt.title('revsym')
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

ax = fig.add_subplot(2,3,6)
ax.scatter(revsym[:,1], revsym[:,2])
plt.xlabel('y')
plt.ylabel('z',labelpad=0)
ax.set_xlim(-0.5,0.5)
ax.set_ylim(-0.5,0.5)

for ax in fig.axes:
  ax.set_xlim(-1.5,1.5)
  ax.set_ylim(-1.5,1.5)

plt.savefig('avg_coms.png')










