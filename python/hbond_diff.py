#! /usr/bin/python

file1="hb2.dat"
file2="hb1.dat"
outf="h_diff.txt"

f=open(outf, 'w')
f.write("Hbonds in %s but not in %s \n" %(file1, file2))

with open(file1) as ifile:
    lines1 = ifile.readlines()
lines1=lines1[1:]
lines1=[line for line in lines1 if line.strip()]   
with open(file2) as ifile:
    lines2 = ifile.readlines()
lines2=lines2[1:]
lines2=[line for line in lines2 if line.strip()]

for line1 in lines1:
  hbond_exists=False
  line1sp=line1.split()
  for line2 in lines2:
    line2sp=line2.strip().split()
    if line1sp[0] == line2sp[0] and line1sp[1]==line2sp[1] and line1sp[2]==line2sp[2]:
      hbond_exists=True
      break
  if hbond_exists==False:    
    f.write(line1)
