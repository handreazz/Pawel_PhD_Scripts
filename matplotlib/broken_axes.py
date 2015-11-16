#! /usr/bin/python
from numpy import *
import sys
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("poster")

files= ["clashscore.dat", "molprobity.dat", 
      "ramachandran_favored.dat", "ramachandran_outliers.dat",
      "rmsd_angles.dat", "rmsd_bonds.dat", "rotamer_outliers.dat"]
      
print "Percent of models lower with amber:"
for filename in files:
  data=genfromtxt(filename, skip_header=1)
  total=data.shape[0]
  amber_lower=sum(data[:,1]<data[:,0])
  amber_lower_percent=float(amber_lower)/total *100
  mean_decrease=0
  for i in range(total):
    if data[i,0] !=0:
      mean_decrease+=100-data[i,1]/data[i,0]*100
  mean_decrease= mean_decrease/total    
  print "%s: %5.2f mean_decrease: %5.2f" %(filename, amber_lower_percent, mean_decrease)

data=genfromtxt('hbond_summary3.0')
total=data.shape[0]
amber_lower=sum(data[:,1]<data[:,2])
amber_lower_percent=float(amber_lower)/total *100
mean_decrease=0
for i in range(total):
  if data[i,1] !=0:
    mean_decrease+=data[i,2]/data[i,1]*100
mean_decrease= mean_decrease/total    
print "hbond: %5.2f mean_increase: %5.2f" %(amber_lower_percent, mean_decrease)
  
  

clash=genfromtxt('clashscore.dat', skip_header=1)
molp=genfromtxt('molprobity.dat', skip_header=1)
ramaf=genfromtxt('ramachandran_favored.dat', skip_header=1)
ramao=genfromtxt('ramachandran_outliers.dat', skip_header=1)
hbond=genfromtxt('hbond_summary3.0')

#~ plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
#~ plt.rc('axes',linewidth=3)
#~ plt.rc('legend', fontsize=20) 
#~ plt.rc('lines', markeredgewidth=2)
#~ plt.rc('xtick.minor',size=5)
#~ plt.rc('xtick.major',size=10)
#~ plt.rc('lines', linewidth=3) 
#~ fig=plt.figure(figsize=(16, 12))
#~ ax = fig.add_subplot(111)

plt.scatter(clash[:,0], clash[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,20))
plt.ylim((0,20))
plt.ylabel('Amber')
plt.xlabel('Engh-Huber')
plt.title('Clash Scores')
#~ plt.show()
plt.savefig("clash.jpg")
plt.close()

plt.scatter(molp[:,0], molp[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,3.5))
plt.ylim((0,3.5))
plt.ylabel('Amber')
plt.xlabel('Engh-Huber')
plt.title('Molprobity Scores')
#~ plt.show()
plt.savefig("molp.jpg")
plt.close()

plt.scatter(ramaf[:,0], ramaf[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((70,100))
plt.ylim((70,100))
plt.ylabel('Amber')
plt.xlabel('Engh-Huber')
plt.title('Ramachandran Favored')
#~ plt.show()
plt.savefig("ramaf.jpg")
plt.close()

plt.scatter(ramao[:,0], ramao[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,7))
plt.ylim((0,7))
plt.ylabel('Amber')
plt.xlabel('Engh-Huber')
plt.title('Ramachandran Outliers')
#~ plt.show()
plt.savefig("ramao.jpg")
plt.close()

plt.scatter(hbond[:,1], hbond[:,2])
plt.plot([0,2000], [0,2000], c='k', linewidth=1)
plt.xlim((0,1600))
plt.ylim((0,1600))
plt.ylabel('Amber')
plt.xlabel('Engh-Huber')
plt.title('Hydrogen Bonds')
#~ plt.show()
plt.savefig("hbond.jpg")
plt.close()

plt.scatter(clash[:,0], clash[:,1], c='b' )
plt.scatter(molp[:,0], molp[:,1], c='g')
#~ plt.scatter(ramaf[:,0], ramaf[:,1], c='r')
plt.scatter(ramao[:,0], ramao[:,1], c='#A020F0')
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,15))
plt.ylim((0,15))
#~ plt.show()
plt.savefig("all.jpg")
plt.close()


fig = plt.figure()
fig.subplots_adjust(wspace=.05,right=.95, left=.05,top=.93, bottom=.05, hspace=.05)
ax1 = plt.subplot(221)
ax1.set_xlim(0,11)
ax1.set_ylim(68,100)
ax2 = plt.subplot(222)
ax2.set_xlim(68,100)
ax2.set_ylim(68,100)
ax3 = plt.subplot(223)
ax3.set_xlim(0,11)
ax3.set_ylim(0,11)
ax4 = plt.subplot(224)
ax4.set_xlim(68,100)
ax4.set_ylim(0,11)

ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax4.spines['top'].set_visible(False)
ax4.spines['left'].set_visible(False)

ax1.tick_params(labelbottom='off')
ax2.tick_params(labelbottom='off')
ax2.tick_params(labelleft='off')
ax2.tick_params(labelright='on')
ax4.tick_params(labelleft='off')
ax4.tick_params(labelright='on')

ax3.scatter(molp[:,0], molp[:,1], c='g')
ax3.scatter(clash[:,0], clash[:,1], c='b' )
ax3.scatter(ramao[:,0], ramao[:,1], c='#A020F0')
ax2.scatter(ramaf[:,0], ramaf[:,1], c='r')
ax2.plot([0,100], [0,100], c='k', linewidth=1)
ax3.plot([0,100], [0,100], c='k', linewidth=1)

d = .015 # how big to make the diagonal lines in axes coordinates
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((-d,+d),(-d,+d), **kwargs)      # bottom-left
ax1.plot((1-d,1+d),(1-d,1+d), **kwargs) # top-right

kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
ax2.plot((-d,+d),(1-d,1+d), **kwargs)   # top-left
ax2.plot((1-d,1+d),(-d,+d), **kwargs)    # bottom-right
ax2.plot((-d,+d),(+d,-d), **kwargs)      # bottom-left

kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
ax3.plot((-d,+d),(1-d,1+d), **kwargs)   # top-left
ax3.plot((1-d,1+d),(1+d,1-d), **kwargs) # top-right
ax3.plot((1-d,1+d),(-d,+d), **kwargs)    # bottom-right

kwargs = dict(transform=ax4.transAxes, color='k', clip_on=False)
ax4.plot((-d,+d),(-d,+d), **kwargs)      # bottom-left
ax4.plot((1-d,1+d),(1-d,1+d), **kwargs) # top-right


plt.savefig('all2.jpg')
