#! /usr/bin/python
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import sys

plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
plt.rc('axes',linewidth=3)
plt.rc('legend', fontsize=20) 
plt.rc('lines', markeredgewidth=2)
plt.rc('xtick.minor',size=5)
plt.rc('xtick.major',size=10)
plt.rc('lines', linewidth=3) 
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


tyr=genfromtxt("for_plot_tyr.txt", skip_header=2)
gyges=genfromtxt("for_plot_gyges.txt", skip_header=2)



fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.plot(tyr[:,0],tyr[:,1], '-o', color='b', label='Tyr' )
ax.plot(gyges[:,0],gyges[:,1], '-o', color='r',  label='Gyges' )
ax.set_xticks([1,2,4,8,16,32,48])
plt.xlim((0,50))
plt.ylim((0,200))
lgd=ax.legend(loc=5, title=r'FFT CPU Time', bbox_to_anchor=(.80, .915))
lgd.get_title().set_fontsize(20)



ax2 = ax.twinx()
ax2.plot(tyr[:,0],tyr[:,3], '-o', color=colors[2], label='Tyr' )
ax2.plot(gyges[:,0],gyges[:,3], '-o', color=colors[3], label='Gyges' )
lgd=ax2.legend(loc=1, title='Total CPU Time')
lgd.get_title().set_fontsize(20)
plt.ylim((0,4000))


ax.set_xlabel("No. shared-memory threads", fontsize=16)
ax.set_ylabel("FFT CPU time (s)", fontsize=16)
ax2.set_ylabel("Total CPU time (s)", fontsize=16)

plt.show()
