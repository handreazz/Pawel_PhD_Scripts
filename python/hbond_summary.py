#! /usr/bin/python

import os

location='/home/pawelrc/work/Gordon_2014/geo_min_plots'

#locate dirs with 'name_geom_min_amber.pdb' file
rootdirs=os.walk(location).next()[1]
gooddirs=[]
for rootdir in rootdirs:
  files=os.walk('%s/%s' %(location,rootdir)).next()[2]
  if '%s_geom_min_amber.pdb' %rootdir in files:
    gooddirs.append(rootdir)

#summary file
g=open('hbond_summary','w')

#iterate over all directories where amber worked
for dir in gooddirs:
  #amber hbonds
  f=open('ctraj_in', 'w')
  f.write('parm %s/%s/%s.prmtop\n' %(location,dir,dir))
  f.write('trajin %s/%s/%s_geom_min_amber.pdb\n' %(location, dir,dir))
  f.write('hbond out nhb_%s_amber.dat\n' %dir)
  f.close()
  os.system('cpptraj -i ctraj_in')
  #phenix hbonds
  f=open('ctraj_in', 'w')
  f.write('parm %s/%s/%s.prmtop\n' %(location,dir,dir))
  f.write('trajin %s/%s/%s_geom_min.pdb\n' %(location, dir,dir))
  f.write('hbond out nhb_%s.dat\n' %dir)
  f.close()
  os.system('cpptraj -i ctraj_in')
  #read hbond results
  with open('nhb_%s_amber.dat' %dir) as ifile:
    n_hb_amber= ifile.readlines()[1].split()[1]
  with open('nhb_%s.dat' %dir) as ifile:
    n_hb_phenix= ifile.readlines()[1].split()[1]  
  #write to summary
  g.write('%s %s %s\n' %(dir, n_hb_phenix, n_hb_amber))
  


g.close()
