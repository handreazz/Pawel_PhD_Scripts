#! /usr/bin/python
import sys
import os
from numpy import *


frames=5161
data=zeros((frames*12,4))
for ASU in range(12):
  data[ASU*frames:ASU*frames+frames,1:4]=genfromtxt('com_revsym_%02d_01.dat' %(ASU+1))
savetxt('com.dat',data,fmt='%10.4f')



means, vars, maes, rmsds, maes_std =[], [], [], [], []

#function to get distance
def dist(posc, meanc):
  return sqrt((posc[0]-meanc[0])**2+(posc[1]-meanc[1])**2+(posc[2]-meanc[2])**2)
  
"""
for each ASU
  meannow= center of mass of the ASU
  devnow= array of all center of mass deviations from mean center of mass
  mae= mean deviation
  rmsd= root mean square deviation
for all ASU
  means = array of centers of mass, one for each asu
  maes = array of mean deviations, one for each ASU
  maes_std = array of std deviations of the mean deviations, one for each ASU
  rmsds = array of root mean square deviations, one for each ASU
"""
for ASU in range(12):
  datanow=data[ASU*frames:ASU*frames+frames,:]
  meannow=mean(datanow[:,1:4],axis=0)
  devnow=array([ dist(row[1:4], meannow) for row in datanow]) 
  mae= mean(devnow)
  mae_std=std(devnow)
  rmsd=sqrt(mean(devnow**2))
  means.append(meannow)
  maes.append(mae)
  maes_std.append(mae_std)
  rmsds.append(rmsd)


print "within ASU"
print mean (maes), mean(rmsds), mean(maes_std)


"""
For entire dataset:
  meanall - center of mass
  devall - array of all deviations from the overall center of mass
  mae - mean deviation
  mae_std - std deviation of the mean deviation
  rmsd - root mean square deviation
"""
print "all data"
meanall=mean(data[:,1:4],axis=0)
devall=array([ dist(row[1:4], meanall) for row in data])
mae= mean(devall)
mae_std= std(devall)
rmsd=sqrt(mean(devall**2))
print mae, rmsd, mae_std
import code; code.interact(local=dict(globals(), **locals()))

"""
  meanbet - mean of the 12 mean centers of mass
  devbet - array of deviatios of the ASU mean centers of mass from the overall mean center of mass
  maebet - mean deviation of ASU centers of mass from overall center of mass
  rmsdbet - root mean square deviation of "
"""
print "between ASU"
meanbet=mean(means,axis=0)
exp_mean=array([-1.0442,14.3708,24.0721])
exp_devbet=mean(array([ dist(row, exp_mean) for row in means]))
print meanbet-exp_mean, exp_devbet
devbet=array([ dist(row, meanbet) for row in means])
maebet= mean(devbet)
maebet_std=std(devbet)
rmsdbet=sqrt(mean(devbet**2))  
print maebet, rmsdbet, maebet_std


#~ for i in means:
  #~ print i
#Calculate the mean distance between any two ASU mean centers of mass
dev=[]
for i in range(12):
  for j in range(i+1,12):
    dev.append(dist(means[i],means[j]))
print mean(dev)    
#Calculate the mean distance between the instantaneous ASU center of mass and it's mean center of mass
print mean (maes)


#~ shifts=genfromtxt("com_shifts.dat")
#~ shifts=shifts[:,1:4]
#~ meandev=0
#~ count=0
#~ for i in range(61932):
  #~ for j in range(i+1,61932):
    #~ meandev+=dist(shifts[i],shifts[j])/1917755346.0
    #~ count+=1
#~ print meandev
#~ print count
