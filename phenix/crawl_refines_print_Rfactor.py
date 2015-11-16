import os
import glob

dbase="/media/My Book/Marco/rigi_145392/p6522"
ds = next(os.walk(dbase))[1]
ds = [i for i in ds if i.startswith('Refine')]
f = lambda x: (x,int(x.split('_')[-1]))
ds = map(f,ds)
ds.sort(key=lambda x: x[-1])
ds = [ i[0] for i in ds ]

for d in ds:
  logfile = glob.glob('%s/%s/*log' %(dbase,d))
  if len(logfile) ==0:
    continue
  f=open(logfile[0], 'r')
  l=f.readlines()
  print d
  print l[-2],
  print l[-1]