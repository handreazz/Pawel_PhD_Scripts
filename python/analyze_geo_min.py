#! /usr/bin/python
from numpy import *
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
  

clash=genfromtxt('clashscore.dat', skip_header=1)
molp=genfromtxt('molprobity.dat', skip_header=1)
ramaf=genfromtxt('ramachandran_favored.dat', skip_header=1)
ramao=genfromtxt('ramachandran_outliers.dat', skip_header=1)

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
#~ plt.show()
plt.savefig("clash.jpg")
plt.close()

plt.scatter(molp[:,0], molp[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,3.5))
plt.ylim((0,3.5))
#~ plt.show()
plt.savefig("molp.jpg")
plt.close()

plt.scatter(ramaf[:,0], ramaf[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((70,100))
plt.ylim((70,100))
#~ plt.show()
plt.savefig("ramaf.jpg")
plt.close()

plt.scatter(ramao[:,0], ramao[:,1])
plt.plot([0,100], [0,100], c='k', linewidth=1)
plt.xlim((0,7))
plt.ylim((0,7))
#~ plt.show()
plt.savefig("ramao.jpg")
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

