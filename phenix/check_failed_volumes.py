import os, sys
import ReadAmberFiles as raf
import numpy as np

#~ f=open('1a21/list_amber_fails.txt','r')
#~ fails=[]
#~ for line in f.readlines():
  #~ if line.strip():
    #~ fails.append( line.strip().split('/')[0] )

fails=['1a21', '1a8v', '1ba7', '1c03', '1dvm', '1ezs', '1f3u', '1fc3', 
       '1fh5', '1jxo', '1ofp', '1oy3', '1q32', '1q4o', '1r19', '1r1z', 
      '1r52', '1rzi', '1t0j', '1tee', '1tks', '1tw9', '1tzo', '1vh0', 
      '1vr4', '1w3b', '1wp7', '1wp8', '1x13']


dirs=[ name for name in os.listdir('.') if os.path.isdir(name) and name[0]=='1' ]
bad=[]
good=[]
for dir in dirs:
  if dir in fails:
    print dir
    trst=raf.rst7('%s/%s.rst7' %(dir,dir))
    box=trst.Get_Box()
    bad.append( raf.Get_volume(box) )
  else:
    print dir
    trst=raf.rst7('%s/%s.rst7' %(dir,dir))
    box=trst.Get_Box()
    good.append( raf.Get_volume(box) )

print "BAD: mean %1.0f\n" %(np.mean(bad))
for v in bad:
  print "%d\n" %v

print "\n"

print "GOOD: mean %1.0f\n" %(np.mean(good))
for v in good:
  print "%d\n" %v
    

