#! /usr/bin/python
import os, sys


def remove_waters(wats,di):
  newlines=[]
  with open("fav8_sc.pdb") as f:
    lines=f.readlines()
    n=0
    while n<len(lines):
      if lines[n][0:4]=='ATOM':
        if int(lines[n][23:26]) in wats:
          n+=4
          continue
      newlines.append(lines[n])    
      n+=1
    outf=open("74.pdb",'w')
    outf.writelines(newlines)
    outf.close()   
  os.system('mv 74.pdb %s' %di)

#~ 7
  #~ don't remove anything
#~ 6.5
  #~ remove wat24 from UC1-9 and 19-27
wats=[]
for i in range(0,9):
  wats.append(724+i*7)
for i in range(18,27):
  wats.append(724+i*7)
remove_waters(wats,'6.5')
  

#~ 6
  #~ remove all instances of wat24
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
remove_waters(wats,'6')
  
#~ 5.5
  #~ remove wat24, wat26 from UC1-9 and 19-27
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
for i in range(0,9):
  wats.append(726+i*7)
for i in range(18,27):
  wats.append(726+i*7)
remove_waters(wats,'5.5')
  
#~ 5.0
  #~ remove wat24,wat26 from all UC
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
  wats.append(726+i*7)
remove_waters(wats,'5')
  
#~ 4.5
  #~ remove wat 24, 26, 23 from UC1-9 and 19-27
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
  wats.append(726+i*7)
for i in range(0,9):
  wats.append(723+i*7)
for i in range(18,27):
  wats.append(723+i*7)
remove_waters(wats,'4.5')

#~ 4.25
  #~ remove wat 24,26,23 from UC10-36
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
  wats.append(726+i*7)
for i in range(9,36):
  wats.append(723+i*7)
remove_waters(wats,'4.25')

#~ 4.00
  #~ remove wat 24,26,23 from UC1-36
wats=[]
for i in range(0,36):
  wats.append(724+i*7)
  wats.append(726+i*7)
  wats.append(723+i*7)
remove_waters(wats,'4')



