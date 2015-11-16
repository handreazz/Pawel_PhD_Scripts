#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from smooth_signal import smooth

file=sys.argv[1]  #eg residContact_summary/x,y+1,z
ASUS=12

f=open(file,'r')
contact_names=f.readline().split()
f.close()
all_data=genfromtxt(file,skip_header=1)
iface=file.split('/')[-1]
os.system("mkdir -p residContact_plots_tmp")
os.system("mkdir -p residContact_plots_tmp/%s" %iface)

totalp=0.0
contactp=0
print "crystal contacts:"
for i in range(len(contact_names)):
    name=contact_names[i]
    data=all_data[:,i]
    totalp+=average(data)
    if data[-1]==ASUS:
      print name
      is_cryst=1
    else:
      is_cryst=0
    if average(data) <4 and is_cryst!=1:
        continue
    fig=plt.figure(figsize=(16, 12))
    plt.ylim((0,ASUS+1))
    ax = fig.add_subplot(111)  
    ax.plot(smooth(data,10),'k')
    plt.title('%s' %name, fontsize=24)
    fig.suptitle('%s' %iface, fontsize=18)
    plt.legend(["%5.2f" %average(data)])
    contactp+=1
    if is_cryst:
      plt.annotate('crystal contact',xy=(5000,12.1), xytext=(5000,12.1),fontsize=18)
    plt.savefig('residContact_plots_tmp/%s/%s.png' %(iface,name))

#~ totalp=totalp/contactp
#~ totalp=totalp/
print "%s %5.4f\n" %(iface, totalp)
