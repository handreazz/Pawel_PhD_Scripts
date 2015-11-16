
  

  
import os, glob, sys
from libtbx import easy_run

idir = "/home/pawelrc/Data/work/Phenix/"

f=open('clash_summary.txt','w')

f.write('    pre-refine       scale0.90Amber\n')
for x in os.listdir(idir):
    if os.path.isfile(idir+x): continue
    if len(x) != 4: continue
    infile = idir+'%s/%s.pdb' %(x,x)
    f.write('%s ' %x)
    if os.path.isfile(infile):
      print infile
      cmd='phenix.clashscore %s' %infile
      print cmd
      ero=easy_run.fully_buffered(cmd)
      assert (ero.return_code == 0)
      cscore = ero.stdout_lines[-1].split()[-1]
      f.write('%8s ' %cscore)
    infile = idir+'%s/%s_refine_scale_0.090_001.pdb' %(x,x)
    if os.path.isfile(infile):
      print infile
      cmd='phenix.clashscore %s' %infile
      print cmd
      ero=easy_run.fully_buffered(cmd)
      assert (ero.return_code == 0)
      cscore = ero.stdout_lines[-1].split()[-1]
      f.write('%8s ' %cscore)
      
      cmd = "grep \'wxc =\' %s%s/%s_refine_scale_0.090_001.log" %(idir,x,x)
      print cmd
      ero=easy_run.fully_buffered(cmd)
      wxc = ero.stdout_lines[0].split()[2]
      f.write('%s ' %wxc
    f.write('\n')
    
    
f.close()
    

