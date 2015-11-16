#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


##########################################################
#                                                        #
# This will plot diffusion of four simulations at once.  #
#                                                        #
##########################################################

#Variables
data1=genfromtxt('diffusionall_x.xmgr')
data2=genfromtxt('../../RunCase_II/waterdist/diffusionall_x.xmgr')
data3=genfromtxt('../../RunCase_III/waterdist/diffusionall_x.xmgr')
data4=genfromtxt('../../RunCase_IV/waterdist/diffusionall_x.xmgr')

frames1=120001
frames2=80001

#Matlplotlib rc settings
 #padding for tick labels
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
 #thicker axes frame
plt.rc('axes',linewidth=4)
plt.rc('legend', fontsize=20)
 #mathtext font
plt.rc('mathtext',default='regular')

###################################

fig=plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)

## PLOT X-AXIS DIFFUSION


#RunCase_II
x=[]
y=[]
for i in range(frames2/10):  #this is to get average over each 10 frames (.2ns)
	x.append((data2[10*i,0]))
	y.append(average(data2[10*i:10*i+10,1]))
ax.plot(x,y,'#F1BA0D', linewidth=4)

#RunCase_III
x=[]
y=[]
for i in range(frames2/10):  #this is to get average over each 10 frames (.2ns)
	x.append((data3[10*i,0]))
	y.append(average(data3[10*i:10*i+10,1]))
ax.plot(x,y,'#006633', linewidth=4)

#RunCase_IV
x=[]
y=[]
for i in range(frames2/10):  #this is to get average over each 10 frames (.2ns)
	x.append((data4[10*i,0]))
	y.append(average(data4[10*i:10*i+10,1]))
ax.plot(x,y,'#6600cc', linewidth=4)

#RunCase
x=[]
y=[]
for i in range(frames1/10):  #this is to get average over each 10 frames (.2ns)
	x.append((data1[10*i,0]))
	y.append(average(data1[10*i:10*i+10,1]))
ax.plot(x,y,'k', linewidth=4)

#Linear fit 1
#~ x=range(1,450000,10000) #x-axis range
#~ y=map(lambda i:i*0.0007245+2.578,x) #linear formula
#~ ax.plot(x,y,'r', linewidth=4)

##LINEAR FIT
#RunCase
x=range(500000,2400000,10000)
y=map(lambda i:i*0.0001965+241.7,x)
line1=ax.plot(x,y,'k', linewidth=4)

#RunCase_II
x=range(500000,1600000,10000) #x-axis range
y=map(lambda i:i*0.000671+4.335,x)
line2=ax.plot(x,y,'#F1BA0D', linewidth=4)

#RunCase_III
x=range(500000,1600000,10000) #x-axis range
y=map(lambda i:i*0.0005756+1.812,x) #linear formula
line3=ax.plot(x,y,'#006633', linewidth=4)

#RunCase_IV
x=range(500000,1600000,10000) #x-axis range
y=map(lambda i:i*0.0005399+82.83,x)
line4=ax.plot(x,y,'#6600cc', linewidth=4)

for label in ax.xaxis.get_ticklabels():
	label.set_fontsize(24)
for label in ax.yaxis.get_ticklabels():
	label.set_fontsize(24)
#plt.title('',fontsize=28)
plt.xlabel('Time (${\mu}s$)',fontsize=28, labelpad=10)
ax.set_xticklabels([0,0.5,1.0,1.5,2.0,2.5])
plt.ylabel('Mean Square Displacement ($\AA^{2}$)',fontsize=28, labelpad=5)
#plt.ylim(ymax=35)
#plt.xlim(xmax=500)	#modify to trajectory length

ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
for line in ax.get_xticklines() + ax.get_yticklines():
	line.set_markeredgewidth(4)
	line.set_markersize(10)
#~ plt.annotate(r'Slope=$7.2 x 10^{-4}$',xy=(5000,200), xytext=(340000,200),fontsize=28)
#~ plt.annotate('Slope=$2.0 x 10^{-4}$',xy=(5000,200), xytext=(1500000,475),fontsize=28)
#ax.legend(["peptide", "backbone"],bbox_to_anchor=(0, 0, .95, .2))
lgd = ax.legend([line1,line2,line3,line4], ['$2.0 x 10^{-4}$','$6.7 x 10^{-4}$','$5.8 x 10^{-4}$','$5.4 x 10^{-4}$'], numpoints=1,shadow='True',fancybox=True,loc=4,title=r'Slope $(\mathit{\AA^{2}/{\mu}s})$')
lgd.get_title().set_fontsize(24)
#~ for t in lgd.get_texts():
	#~ t.set_fontsize(24)

#~ plt.setp(ltit,fontsize=24)
#~ lgd.get_lines()[0].set_marker('o')
#~ lgd.get_lines()[0].set_linewidth(0)

#~ plt.show()
plt.savefig('diffusion.pdf') 
plt.savefig('diffusion.png')


#~ ###############################################
#~ 
#Figure2
#fig=plt.figure(figsize=(16, 12))
#ax = fig.add_subplot(111)

##plot the x-axis diffusion
#x=[]
#y=[]
#for i in range(frames/10):  #this is to get average over each 10 frames (.2ns)
	#x.append((data1[10*i,0])/1000000)
	#y.append(average(data1[10*i:10*i+10,1]))
#ax.plot(x,y,'b', linewidth=4)

##plot the y-axis diffusion
#x=[]
#y=[]
#for i in range(frames/10):  #this is to get average over each 10 frames (.2ns)
	#x.append((data1[10*i,0])/1000000)
	#y.append(average(data2[10*i:10*i+10,1]))
#ax.plot(x,y,'r', linewidth=4)

##plot the z-axis diffusion
#x=[]
#y=[]
#for i in range(frames/10):  #this is to get average over each 10 frames (.2ns)
	#x.append((data1[10*i,0])/1000000)
	#y.append(average(data3[10*i:10*i+10,1]))
#ax.plot(x,y,'g', linewidth=4)

#for label in ax.xaxis.get_ticklabels():
	#label.set_fontsize(24)
#for label in ax.yaxis.get_ticklabels():
	#label.set_fontsize(24)
##plt.title('',fontsize=28)
#plt.xlabel('Time (${\mu}s$)',fontsize=28, labelpad=10)
##ax.set_xticklabels([0,0.5,1.0,1.5,2.0,2.5])
#plt.ylabel('Mean Square Displacement ($\AA^{2}$)',fontsize=28, labelpad=10)
#plt.ylim(ymax=100)
#plt.xlim(xmax=0.5)	#modify to trajectory length

#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')
#for line in ax.get_xticklines() + ax.get_yticklines():
	#line.set_markeredgewidth(4)
	#line.set_markersize(10)
#ax.legend(["a vector", "b vector", "c vector"],bbox_to_anchor=(0, 0, .95, .95))

##plt.show()
#plt.savefig('diffusion2.png')
#plt.savefig('diffusion2.pdf')
