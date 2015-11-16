#! /usr/bin/python
import os,sys
from numpy import *

#======================================================================#
#                                                                      #
# Analyze output of find_residue_contacts.py. A file is safed for each #
# interface. The file is a matrix with each inter-residue contact found#
# in that interface in the columns and trajectory frames in the rows.  #
# Each entry gives the number of asu's making that contact in that     #
# frame.                                                               #
#                                                                      #
#======================================================================#


# USER SET
# directory with find_residue_contacts output
directory="/net/casegroup2/u2/pjanowsk/Case/4lzt/RunSi/average_density/residueContacts/"
# cotacts with the following residues will be ignored
solvent=['NO3','ACT','H2O','WAT']
# END USER SET


# setup
files=os.listdir(directory)
ifaces={}
stop_at=len(files)
#~ stop_at=1000


class interface:
  def __init__(self,ifacename):
    self.ifacename=ifacename     #iface name
    self.contacts=[]             #list of contact names
    self.all=zeros((1,1))        #array of contact numbers
  def addrow(self):
    cols=self.all.shape[1]
    row=[0]*cols
    self.all=vstack([self.all,row])
  def addcol(self):
    rows=self.all.shape[0]
    col=[[0]]*rows
    self.all=hstack([self.all,col])
 
# find all interfaces, place iface name in ifaces dict keys and
# corresponding interface object as ifaces dict value
print "Setting up iface objects."
for i in files[0:stop_at]:
  f=open(directory+i, 'r')
  for line in f:
    if line.split()[0]=='S':
      ifacename=line.split()[1]
      if ifacename not in ifaces.keys():
        ifaces[ifacename]=interface(ifacename)
        ifaces[ifacename].all=zeros((stop_at,0))
  f.close()

# populate contacts array 
print "\nParsing %d frames." %stop_at
frame=-1
for i in files[0:stop_at]:    
  frame+=1
  ifacename=''
  f=open(directory+i, 'r')
  for line in f:
    # if interface name line, set ifacename
    if line.split()[0]=='S':
      ifacename=line.split()[1]
    # if solvent in contact, skip it  
    elif line.split()[1] in solvent or line.split()[3] in solvent:
      continue
    else:
      # create contact name
      contact=line.split()[0]+line.split()[1]+'-'+line.split()[2]+line.split()[3]
      # if new contact, add to list, add column to array
      if contact not in ifaces[ifacename].contacts:
        ifaces[ifacename].contacts.append(contact)
        ifaces[ifacename].addcol()
      # find column of contact  
      col=ifaces[ifacename].contacts.index(contact)
      # add entry to array
      ifaces[ifacename].all[frame,col]=line.split()[4]
  f.close()


print "\nSaving arrays to disk."
# find only the ifaces that actually have contacts (some ifaces only had
# solvent contacts, so skip those)
populated_ifaces=[]
for ifacename,iface in ifaces.items():
  if len(iface.contacts)>0:
    populated_ifaces.append(ifacename)
print "\nFound interfaces: %d" %len(populated_ifaces)


for ifacename in populated_ifaces:  
  # get the iface
  iface=ifaces[ifacename]
  # print basic stats
  print ifacename
  print( "   Total different residue contacts: %d" %iface.all.shape[1] )
  print( "   Avg no. of contacts per frame: %4.2f" %(mean(sum(iface.all[0:stop_at],axis=1)/12)))
  occup=mean(iface.all[0:stop_at],axis=0)
  print( "   Contacts w/avg occupancy >10: %d" %len(occup[occup>10]) )
  for i in range(iface.all.shape[1]):
    if occup[i]>10:
      print("      %s  %4.2f" %(iface.contacts[i],occup[i]))
  # save array to file with header line of contact names
  f=open(ifacename, 'w')
  for contact in iface.contacts:
    f.write("%15s   " %contact)
  f.write("\n")
  for row in range(iface.all.shape[0]):  
    for col in range(iface.all.shape[1]):
      f.write("%15d   " %iface.all[row,col])
    f.write("\n")  
  f.close()


      
    
