#! /usr/bin/python
import sys
import os
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


####################################
# set up general variables         #
####################################
Nres=139

class Interface:
  'Interface description includes interacting ASUs, bonds, residues'
  def __init__(self,ASU=[],HB_cryst=[],HB_sim=[],IFACE=[],name='noname'):
    self.ASU=ASU
    self.HB_cryst=HB_cryst
    self.HB_sim=HB_sim
    self.IFACE=IFACE
    self.name=name
#Y
Y=Interface(name='Y')
Y.ASU=[ \
[1,3],[3,1], \
[2,4],[4,2], \
[5,7],[7,5], \
[6,8],[8,6], \
[9,11],[11,9], \
[10,12],[12,10], \
]

Y.HB_cryst=[ \
[':21@NH2',':66@O'], \
[':19@ND2',':81@O'], \
]

Y.HB_sim=[ \
[':19@ND2',':84@O'], \
[':19@OD1',':41@NE2'], \
[':23@OH',':68@NH1'], \
[':21@O',':68@NH1'], \
[':21@O',':68@NH2'], \
]

Y.IFACE=[ \
'2,39,41,43,45,53,66-68,81,84,85', \
'18,19,21-24,27,99,102-104,106,111,116,117,121,124', \
]

#X
X=Interface(name='X')
X.ASU=[ \
[1,5],[5,9],[9,1], \
[2,6],[6,10],[10,2], \
[3,7],[7,11],[11,3], \
[4,8],[8,12],[12,4], \
]

X.HB_cryst=[ \
[':45@O',':77@ND2'], \
[':46@O',':77@ND2'], \
[':37@ND2',':14@O'], \
[':114@NH1',':16@O'], \
[':114@NH2',':18@O'], \
]

X.HB_sim=[ \
[':47@OG1',':75@O'], \
[':47@OG1',':97@NZ'], \
[':47@OG1',':77@ND2'], \
[':113@OD1',':21@NH1'], \
]

X.IFACE=[ \
'33,34,37,44-47,113,114', \
'14-16,18-21,73-77,96-97', \
]

#Z
Z=Interface(name='Z')
Z.ASU=[ \
[1,2], [2,1], \
[3,4], [4,3], \
[5,6], [6,5], \
[7,8],[8,7], \
[9,10],[10,9], \
[11,12],[12,11], \
]

Z.HB_cryst=[ \
[':100@OG',':128@NH1'], \
[':101@O',':5@NH2'], \
[':73@NH1',':3@O'], \
]

Z.HB_sim=[ \
[':102@N',':126@O'], \
[':97@NZ',':7@OE1'], \
]

Z.IFACE=[ \
'2-7,33,37,38,125-128', \
'20,21,62,71-73,75,97,100-103', \
]

#XZ
XZ=Interface(name='XZ')
XZ.ASU=[ \
[1,6],[2,5], \
[5,10],[6,9], \
[9,2],[10,1], \
[3,8],[7,12], \
[11,4],[4,7], \
[8,11],[12,3], \
]

XZ.HB_cryst=[ \
[':47@O',':1@NZ'], \
[':48@OD2',':14@NH1'], \
[':48@OD2',':14@NH2'], \
]

XZ.HB_sim=[ \
[':52@OD1',':128@NH1'], \
[':52@OD2',':128@NH1'], \
[':52@OD1',':128@NH2'], \
[':52@OD2',':128@NH2'], \
[':106@O',':128@NH1'], \
[':106@O',':128@NH2'], \
]

XZ.IFACE=[ \
'47,48,61,62,109,112,113', \
'7,14,128,129', \
]

#XY
XY=Interface(name='XY')
XY.ASU=[ \
[1,7],[2,8], \
[5,11],[6,12], \
[9,3],[10,4], \
[3,5],[4,6], \
[7,9],[8,10], \
[11,1],[12,2], \
]

XY.HB_cryst=[ \
[':113@O',':81@OG'], \
[':116@NZ',':77@OD1'], \
]

XY.HB_sim=[ \
[':119@N',':87@OD1'], \
[':119@N',':87@OD2'], \
]

XY.IFACE=[ \
'112-114,116-117', \
'65,74,77-79,81,82,85,87,89,90,93', \
]

#YZ
YZ=Interface(name='YZ')
YZ.ASU=[ \
[2,3],[3,2], \
[1,4],[4,1], \
[6,7],[7,6], \
[5,8],[8,5], \
[10,11],[11,10], \
[9,12],[12,9], \
]

YZ.HB_cryst=[]
YZ.HB_sim=[]

YZ.IFACE=[ \
'67-71', \
'119,121,125-126', \
]


interfaces=[Y,Z,X,XZ,XY,YZ]
  
#####################################
# GENERAL PLOT SETTINGS             #
#####################################
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=15)
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


#########################################################################
##                                                                      #
##       Plot com distances on separate pages                           #
##                                                                      #
#########################################################################
#def MakePlot(mask,title,filename):
  #fig=plt.figure(figsize=(16, 12))
  #ax = fig.add_subplot(111)
  #import commands
  #files=commands.getoutput(mask).split()
  #for index, file in enumerate(files):
    #residues=file.split('_')
    #residues=[i for i in residues if 'ASU' in i]
    #residues=residues[0].split('ASU')
    #data=genfromtxt(file)
    #ax.plot(data[:,0],data[:,1],colors[index],linewidth=2,label=file)
    
  #ax.plot ([1,data[-1,0]],[data[0,1],data[0,1]],'k',linewidth=4) 
  #for label in ax.xaxis.get_ticklabels():
    #label.set_fontsize(24)
  #for label in ax.yaxis.get_ticklabels():
    #label.set_fontsize(24)
  #plt.title(title,fontsize=28)
  #plt.xlabel('Time (ns)',fontsize=28, labelpad=10)
  ##ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
  #plt.ylabel(r"Distace ($\AA$)",fontsize=28, labelpad=10)
  ##~ plt.ylim((0,6))
  ##plt.xlim(xmax=51) #modify to trajectory length
  #ax.yaxis.set_ticks_position('left')
  #ax.xaxis.set_ticks_position('bottom')
  #for line in ax.get_xticklines() + ax.get_yticklines():
    #line.set_markeredgewidth(4)
    #line.set_markersize(10)
  #from matplotlib.font_manager import fontManager, FontProperties
  #font=FontProperties(size=18)
  ##~ ax.legend()
  ##~ ax.legend(bbox_to_anchor=(0, 0, .95, .2),prop=font,ncol=2)
  #plt.show()
  ##~ plt.savefig(filename) 
  
#for i in ['X','Y','Z','XZ','XY','YZ']:
    ##~ MakePlot('ls output/%s_*_com' %i, '%s interface ASU center of mass change' %i,'plots/%s_ASUcom.png' %i)
    #MakePlot('ls output/%s_*IfaceCom' %i, '%s interface residues center of mass change' %i,'plots/%s_IfaceCom.png' %i)



########################################################################
#                                                                      #
#       PLOT com interface  and ASU distances on one page              #
#                                                                      #
########################################################################
from smooth_signal import smooth
def MakePlot(mask,title,filename):
  fig=plt.figure(figsize=(16, 12))
  fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
  for iface_index,iface_name in enumerate(['X','Y','Z','XZ','XY','YZ']):
    ax = fig.add_subplot(3,2,iface_index+1)
    import commands
    files=commands.getoutput(mask %iface_name).split()
    
    for index, file in enumerate(files):
      residues=file.split('_')
      residues=[i for i in residues if 'ASU' in i]
      residues=residues[0].split('ASU')
      data=genfromtxt(file)
      plot_label=[i for i in file.split('_') if 'ASU' in i][0]
      ax.plot(data[1:,0]*0.2,smooth(data[:,1],50),colors[index],linewidth=2,label=plot_label)
    
    ax.plot ([1,data[-1,0]*0.2],[data[0,1],data[0,1]],'k',linewidth=2) 
    for label in ax.xaxis.get_ticklabels():
      label.set_fontsize(8)
    for label in ax.yaxis.get_ticklabels():
      label.set_fontsize(8)
    plt.title(title %iface_name,fontsize=12)
    plt.xlabel('Time (ns)',fontsize=8, labelpad=0)
    #ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
    plt.ylabel(r"Distace ($\AA$)",fontsize=8, labelpad=0)
    #~ plt.ylim((0,6))
    #plt.xlim(xmax=51) #modify to trajectory length
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    for line in ax.get_xticklines() + ax.get_yticklines():
      line.set_markeredgewidth(4)
      line.set_markersize(10)
    from matplotlib.font_manager import fontManager, FontProperties
    font=FontProperties(size=8)
    if iface_index==5:
      ax.legend(bbox_to_anchor=(0, 0, 1.1, .3),prop=font,ncol=3)
  #~ plt.show()
  plt.savefig(filename) 
  

MakePlot('ls output/%s_*_com', '%s interface ASU center of mass change','plots/ASUcom.png')
#~ MakePlot('ls output/%s_*IfaceCom', '%s interface residues center of mass change','plots/IfaceCom.png')
#~ MakePlot('ls output/%s_*_com', '%s interface ASU center of mass change','ASUcom.png')

########################################################################
#                                                                      #
#       PLOT com interface  and ASU distances on one page              #
#                                                                      #
########################################################################
from smooth_signal import smooth
def MakePlot(mask,title,filename):
  fig=plt.figure(figsize=(16, 12))
  fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
  for iface_index,iface_name in enumerate(['X','Y','Z','XZ','XY','YZ']):
    ax = fig.add_subplot(3,2,iface_index+1)
    import commands
    files=commands.getoutput(mask %iface_name).split()
    
    for index, file in enumerate(files):
      residues=file.split('_')
      residues=[i for i in residues if 'ASU' in i]
      residues=residues[0].split('ASU')
      data=genfromtxt(file)
      if index==0:
        tot_data=[0*len(data[:,1])]
      tot_data+=data[:,1]  
      #~ plot_label=[i for i in file.split('_') if 'ASU' in i][0]
    tot_data=tot_data/(len(files))
    ax.plot(data[0:,0]*0.2,tot_data,'k',linewidth=2)
    print mean(tot_data)
    
    ax.plot ([1,data[-1,0]*0.2],[data[0,1],data[0,1]],'k',linewidth=2) 
    print data[0,1]
    for label in ax.xaxis.get_ticklabels():
      label.set_fontsize(8)
    for label in ax.yaxis.get_ticklabels():
      label.set_fontsize(8)
    plt.title(title %iface_name,fontsize=12)
    plt.xlabel('Time (ns)',fontsize=8, labelpad=0)
    #ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
    plt.ylabel(r"Distace ($\AA$)",fontsize=8, labelpad=0)
    plt.ylim(( data[0,1]-0.5,data[0,1]+0.5 ))
    #plt.xlim(xmax=51) #modify to trajectory length
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    for line in ax.get_xticklines() + ax.get_yticklines():
      line.set_markeredgewidth(4)
      line.set_markersize(10)
    from matplotlib.font_manager import fontManager, FontProperties
    font=FontProperties(size=8)
    #~ if iface_index==5:
      #~ ax.legend(bbox_to_anchor=(0, 0, 1.1, .3),prop=font,ncol=3)
  #~ plt.show()
  plt.savefig(filename) 
  

MakePlot('ls output/%s_*_com', '%s interface ASU center of mass change','plots/ASUcom_avg.png')
#~ MakePlot('ls output/%s_*IfaceCom', '%s interface residues center of mass change','plots/IfaceCom.png')
#~ MakePlot('ls output/%s_*_com', '%s interface ASU center of mass change','ASUcom.png')


#########################################################################
##                                                                      #
##       PLOT sim and cryst h-bond distances (all ASU on one plot)      #
##                                                                      #
#########################################################################

#def MakePlot(iface,crystORsim):
  #fig=plt.figure(figsize=(16, 12))
  #fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
  #fig.suptitle('%s interface %s bonds'%(iface.name,crystORsim))
  #if crystORsim == 'sim':
    #bonds=iface.HB_sim
  #elif crystORsim == 'cryst':
    #bonds=iface.HB_cryst 
    
  #for index,bond in enumerate(bonds):
    #ax = fig.add_subplot(3,2,index+1)  
    #title=bond[0]+bond[1]
    ##~ print title
    #for pair_index,pair in enumerate(iface.ASU):
      #ASU1=pair[0]
      #ASU2=pair[1]
      #res1=int(bond[0].split(':')[1].split('@')[0])
      #res2=int(bond[1].split(':')[1].split('@')[0])
      #atm1=bond[0].split(':')[1].split('@')[1]
      #atm2=bond[1].split(':')[1].split('@')[1]
      #res1=res1+Nres*(ASU1-1)
      #res2=res2+Nres*(ASU2-1)
      #mask1=':%d@%s' %(res1,atm1)
      #mask2=':%d@%s' %(res2,atm2)
      #file='output/%s_%dASU%d_%s%s_%s' %(iface.name,ASU1,ASU2,mask1,mask2,crystORsim)
      #data=genfromtxt(file)
      ##~ print data[0,:]
      #plot_label=[i for i in file.split('_') if 'ASU' in i][0]
      #ax.plot(data[:,0],data[:,1],colors[pair_index],linewidth=2,label=plot_label)
    
    #ax.plot ([1,data[-1,0]],[data[0,1],data[0,1]],'k',linewidth=2) 
    #for label in ax.xaxis.get_ticklabels():
      #label.set_fontsize(8)
    #for label in ax.yaxis.get_ticklabels():
      #label.set_fontsize(8)
    #plt.title(title,fontsize=12)
    #plt.xlabel('Time (ns)',fontsize=8, labelpad=0)
    ##ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
    #plt.ylabel(r"Distace ($\AA$)",fontsize=8, labelpad=0)
    ##~ plt.ylim((0,6))
    ##plt.xlim(xmax=51) #modify to trajectory length
    #ax.yaxis.set_ticks_position('left')
    #ax.xaxis.set_ticks_position('bottom')
    #for line in ax.get_xticklines() + ax.get_yticklines():
      #line.set_markeredgewidth(4)
      #line.set_markersize(10)
  #from matplotlib.font_manager import fontManager, FontProperties
  #font=FontProperties(size=8)
  #plt.legend(bbox_to_anchor=(0, 0, 1.1, .3),prop=font,ncol=3)
  ##~ plt.show()
  #plt.savefig('plots/%s_%s.png' %(iface.name,crystORsim))


#interfaces=[Y,Z,X,XZ,XY,YZ]  
#for i in interfaces:
  #MakePlot(i,'sim')
#for i in interfaces:
  #MakePlot(i,'cryst')


#########################################################################
##                                                                      #
##       PLOT one h-bond distance (separate plot for each ASU           #
##                                                                      #
#########################################################################

#def MakePlot(iface,crystORsim):
  #if crystORsim == 'sim':
    #bonds=iface.HB_sim
  #elif crystORsim == 'cryst':
    #bonds=iface.HB_cryst
  #for index,bond in enumerate(bonds):
    #fig=plt.figure(figsize=(16, 12))
    #fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
    #fig.suptitle('%s interface %s bonds'%(iface.name,bond[0]+bond[1]))

    #for pair_index,pair in enumerate(iface.ASU):    

      #ax = fig.add_subplot(4,3,pair_index+1)  
      #title=pair
    ##~ print title

      #ASU1=pair[0]
      #ASU2=pair[1]
      #res1=int(bond[0].split(':')[1].split('@')[0])
      #res2=int(bond[1].split(':')[1].split('@')[0])
      #atm1=bond[0].split(':')[1].split('@')[1]
      #atm2=bond[1].split(':')[1].split('@')[1]
      #res1=res1+Nres*(ASU1-1)
      #res2=res2+Nres*(ASU2-1)
      #mask1=':%d@%s' %(res1,atm1)
      #mask2=':%d@%s' %(res2,atm2)
      #file='output/%s_%dASU%d_%s%s_%s' %(iface.name,ASU1,ASU2,mask1,mask2,crystORsim)
      #data=genfromtxt(file)
      ##~ print data[0,:]
      #plot_label=[i for i in file.split('_') if 'ASU' in i][0]
      #ax.plot(data[:,0],data[:,1],colors[pair_index],linewidth=2,label=plot_label)
    
      #ax.plot ([1,data[-1,0]],[data[0,1],data[0,1]],'k',linewidth=2)  
      #for label in ax.xaxis.get_ticklabels():
        #label.set_fontsize(8)
      #for label in ax.yaxis.get_ticklabels():
        #label.set_fontsize(8)
      #plt.title(title,fontsize=12)
      #plt.xlabel('Time (ns)',fontsize=8, labelpad=0)
      ##ax.set_xticklabels([0,1.0,2.0,3.0,4.0,5.0])
      #plt.ylabel(r"Distace ($\AA$)",fontsize=8, labelpad=0)
      #plt.ylim((0,10))
      ##plt.xlim(xmax=51)  #modify to trajectory length
      #ax.yaxis.set_ticks_position('left')
      #ax.xaxis.set_ticks_position('bottom')
      #for line in ax.get_xticklines() + ax.get_yticklines():
        #line.set_markeredgewidth(4)
        #line.set_markersize(10)
    #from matplotlib.font_manager import fontManager, FontProperties
    #font=FontProperties(size=8)
    #plt.legend(bbox_to_anchor=(0, 0, 1.1, .3),prop=font,ncol=3)
    ##~ plt.show()
    #plt.savefig('plots/%s_%s_%s_%s.png' %(iface.name,mask1,mask2,crystORsim))
##~ MakePlot(X,'sim') 
#interfaces=[Y,Z,X,XZ,XY,YZ]  
#for i in interfaces:
  #MakePlot(i,'sim')
#for i in interfaces:
  #MakePlot(i,'cryst')
