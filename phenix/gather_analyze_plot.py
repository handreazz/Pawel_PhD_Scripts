#! /usr/bin/env python

import os, sys
from numpy import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import seaborn as sns
sns.set_context("poster")
sns.set_style("white")


pdbs_c = []
pdbs = []
with open('mtz.txt', 'r') as f:
  for line in f.readlines():
    pdbs_c.append(line.strip()[0:4])

print "Incomplete refinements:"
for pdb in pdbs_c:
  os.chdir(pdb)
  if os.path.isfile('Summary_%s.dat' %pdb):
    with open('Summary_%s.dat' %pdb) as f:
      lines = f.readlines()
      if len(lines) == 21:
        pdbs.append(pdb)
      elif len(lines) > 1:
        print "  %s %d" %(pdb, len(lines))
  os.chdir('..')
print "Total complete refines:\n  %d\n" %len(pdbs)


data=zeros((20,12, len(pdbs)))
pdb_counter=0
for pdb in pdbs:
  os.chdir(pdb)
  with open('Summary_%s.dat' %pdb) as f:
    f.readline()
    line_counter = 0
    for line in f:
      line = line.strip().split()[1:]
      for i, val in enumerate(line):
        data[line_counter, i, pdb_counter] = val
      line_counter += 1
  pdb_counter += 1
  os.chdir('..')

rows = '''EH
  EH_opt
  noratio_opt
  ratio_opt
  ratio_0.006
  ratio_0.01
  ratio_0.02
  ratio_0.04
  ratio_0.08
  ratio_0.15
  ratio_0.3
  ratio_0.5
  noratio_0.006
  noratio_0.01
  noratio_0.02
  noratio_0.04
  noratio_0.08
  noratio_0.15
  noratio_0.3
  noratio_0.5
  '''.split()

cols = '''Rfree
  clash
  hbond
  MolP_sc
  Rama_outl
  Rama_fav
  Rotam
  Cbeta
  RMS_bnd
  RMS_ang
  Reso
  Rwork
  '''.split()
# i = rows.index('ratio_0.5')
# j = cols.index('Cbeta')

plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=10)
plt.rc('axes',linewidth=3)
plt.rc('legend', fontsize=20)
plt.rc('lines', markeredgewidth=2)
plt.rc('xtick.minor',size=5)
plt.rc('xtick.major',size=10)
plt.rc('lines', linewidth=3)


#line plots
def lineplot(pdb,prop):
  k = pdbs.index(pdb)
  j = cols.index(prop)
  d = data[:,j, k]
  EH_d = d[0]
  EHopt_d = d[1]
  noratio_opt_d = d[2]
  ratio_opt_d = d[3]
  ratio = d[4:12]
  noratio = d[12:20]
  x = [0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5]
  fig=plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111)
  fig.suptitle('%s %s' %(pdb, prop), fontsize=18,y=.95)
  l1 = ax.plot(x, ratio, label='ratio')
  l2 = ax.plot(x, noratio, label='noratio')
  l3 = plt.axhline(y=EH_d, color='r', linewidth=3)
  plt.xlim(0.006,0.5)
  if min(d) == 0:
    if max(d) == 0:
      plt.ylim(-1, 1)
    else:
      plt.ylim(-1, max(d)*1.1)
  else:
    plt.ylim(min(d)-min(d)*.1, max(d)*1.1)
  ax.set_xscale('log', subsx=[0])
  ax.set_xticks([0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5])
  ax.set_xticklabels([0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5])
  ax.yaxis.set_ticks_position('left')
  ax.xaxis.set_ticks_position('bottom')
  for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(2)
    line.set_markersize(5)
  for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(14)
  for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(14)
  ax.set_xlabel('wxc_scale',fontsize=16)
  ax.set_ylabel(prop,fontsize=16, labelpad=5)
  l4 = plt.axhline(y=ratio_opt_d, color='b', linewidth=3, ls='--')
  l5 = plt.axhline(y=noratio_opt_d, color='g', linewidth=3, ls='--')
  l6 = plt.axhline(y=EHopt_d, color='r', linewidth=3, ls='--')
  ax.legend(["ratio", "noratio", "EH", "weight opt"],bbox_to_anchor=(0, 0, .999, .999), fontsize=14)
  plt.savefig('lineplots/%s_%s.png' %(pdb,prop))
  plt.close()

#~ print "lineplots"
#~ for i, pdb in enumerate(pdbs):
  #~ print i+1, pdb
  #~ for prop in cols:
    #~ lineplot(pdb, prop)
  #~ 

#line plots noratio
def lineplot_noratio(pdb,prop):
  k = pdbs.index(pdb)
  j = cols.index(prop)
  d = data[:,j, k]
  EH_d = d[0]
  EHopt_d = d[1]
  noratio_opt_d = d[2]
  ratio_opt_d = d[3]
  ratio = d[4:12]
  noratio = d[12:20]
  x = [0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5]
  fig=plt.figure(figsize=(10, 8))
  ax = fig.add_subplot(111)
  fig.suptitle('%s %s' %(pdb, prop), fontsize=18,y=.95)
  l2 = ax.plot(x, noratio, color='b', label='Amber')
  l3 = plt.axhline(y=EH_d, color='r', linewidth=3)
  plt.xlim(0.006,0.5)
  if min(d) == 0:
    if max(d) == 0:
      plt.ylim(-1, 1)
    else:
      plt.ylim(-1, max(d)*1.1)
  else:
    plt.ylim(min(d)-min(d)*.1, max(d)*1.1)
  ax.set_xscale('log', subsx=[0])
  ax.set_xticks([0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5])
  ax.set_xticklabels([0.006, 0.01, 0.02, 0.04, 0.08, 0.15, 0.3, 0.5])
  ax.yaxis.set_ticks_position('left')
  ax.xaxis.set_ticks_position('bottom')
  for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markeredgewidth(2)
    line.set_markersize(5)
  for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(14)
  for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(14)
  ax.set_xlabel('wxc_scale',fontsize=16, labelpad=5)
  ax.set_ylabel(prop,fontsize=16, labelpad=5)
  l5 = plt.axhline(y=noratio_opt_d, color='b', linewidth=3, ls='--')
  l6 = plt.axhline(y=EHopt_d, color='r', linewidth=3, ls='--')
  ax.legend(["Amber", "EH", "Amber_wght_opt", "EH_wght_opt"],bbox_to_anchor=(0, 0, .999, .999), fontsize=14)
  plt.savefig('lineplots_noratio/%s_%s.png' %(pdb,prop))
  plt.close()

#~ print "lineplots_noratio"
#~ for i, pdb in enumerate(pdbs):
  #~ print i+1, pdb
  #~ for prop in cols:
    #~ lineplot_noratio(pdb, prop)

i=cols.index('Reso')
d = data[0,i,:]
print "Min resolution: %f" %min(d)
print "Max resolution: %f" %max(d)


#statistics
print "statistics"
# row:refine, col:prop
means = average(data,axis=2)
dd=copy(data)
for pdb in range(data.shape[2]):
  for row in range(data.shape[0]):
    dd[row,:,pdb] = dd[row,:,pdb] - data[0,:,pdb]
# row:refine, col:prop
diffmeans = average(dd,axis=2)
# row:refine, col:prop
better = zeros((data.shape[0], data.shape[1]))
for prop in cols:
  #row:refine col:pdb
  j = cols.index(prop)
  d = data[:, j, :]
  for refine in rows:
    i = rows.index(refine)
    if prop in ['hbond', 'Rama_fav']:  
      b = sum(d[i] >= d[0])/float(data.shape[2])*100
    else:
      b = sum(d[i] <= d[0])/float(data.shape[2])*100
    better[i,j] = b
f=open('stats.dat','w')
for prop in cols:
  f.write("%s\n" %prop)
  col = cols.index(prop)
  for refine in ['EH', 'EH_opt', 'noratio_opt', 'noratio_0.02', 'noratio_0.04', 'noratio_0.08']:
    row = rows.index(refine)
    f.write("%-12s %7.4f %7.4f %5.2f\n" %(refine, means[row, col], diffmeans[row, col], better[row, col]))
  f.write("\n")

# rgap
j=cols.index('Rfree')
d_rf = data[:,j,:]
j=cols.index('Rwork')
d_rw = data[:,j,:]
d_rgap = d_rf-d_rw
means = average(d_rgap, axis=1)
dd_rgap=copy(d_rgap)
for row in range(d_rgap.shape[0]):
    dd_rgap[row] = d_rgap[row] - d_rgap[0]
diffmeans = average(dd_rgap,axis=1)    
better = zeros((data.shape[0]))
for i in range(data.shape[0]):
  better[i] = sum(d_rgap[i] <= d_rgap[0])/float(d_rgap.shape[1])*100
f.write('Rgap\n')
for refine in ['EH', 'EH_opt', 'noratio_opt', 'noratio_0.02', 'noratio_0.04', 'noratio_0.08']:
  row = rows.index(refine)
  f.write("%-12s %7.4f %7.4f %5.2f\n" %(refine, means[row], diffmeans[row], better[row]))
f.close()

#violin plots
def violinplot(prop):
  if prop == 'Rgap':
    d= d_rgap.T
    d_dEH = dd_rgap.T
  else:  
    d = data[:, cols.index(prop), :].T
    d_dEH =  copy(d)
    for col in range(20):
      d_dEH[:,col] = d_dEH[:,col] - d[:,0]
  
  try:
    p1 = sns.color_palette('Paired')[0:4]
    p2 = [tuple(i) for i in sns.light_palette("red", 10)]
    p3 = [tuple(i) for i in sns.light_palette("purple", 10)]
    pal =  p1 + p2[1:-1] + p3[1:-1]
    
    
    import code ; code.interact(local=dict(globals(), **locals()))
    ax0 = sns.violinplot(d, names=names, color=pal);
    for label in ax0.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax0.set_ylabel('$%s$' %prop,fontsize=20, labelpad=5)    
    plt.savefig('violinplots/%s_all.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop
  try:
    ax1 = sns.violinplot(d_dEH[:,1:], names = names[1:], color=pal[1:], inner='box');
    for label in ax1.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax1.set_ylabel('$\Delta %s  (vs.EH) $' %prop,fontsize=20, labelpad=5)
    plt.savefig('violinplots/%s_all_diff.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop
  try:
    ax2 = sns.violinplot([d[:,0], d[:,1], d[:,2], d[:,14], d[:,15] ], color=sns.color_palette('pastel'), names=names_red)
    for label in ax2.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax2.set_ylabel('%s' %prop,fontsize=20, labelpad=5)    
    plt.savefig('violinplots/%s_red.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop
  try:
    ax3 = sns.violinplot([d_dEH[:,1], d_dEH[:,2], d_dEH[:,14], d_dEH[:,15]], color=sns.color_palette('pastel')[1:], names=names_red[1:])
    for label in ax3.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax3.set_ylabel('$\Delta %s  (vs.EH) $' %prop,fontsize=20, labelpad=5)
    plt.savefig('violinplots/%s_red_diff.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop
  try:
    ax2 = sns.boxplot([d[:,0], d[:,1], d[:,2], d[:,14], d[:,15]], color=sns.color_palette('pastel'), names=names_red)
    for label in ax2.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax2.set_ylabel('$%s$' %prop,fontsize=20, labelpad=5)
    plt.savefig('violinplots/%s_red_box.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop
  try:
    ax3 = sns.boxplot([d_dEH[:,1], d_dEH[:,2], d_dEH[:,14], d_dEH[:,15]], color=sns.color_palette('pastel')[1:], names=names_red[1:])
    for label in ax3.xaxis.get_ticklabels():
        label.set_fontsize(12)
    ax3.set_ylabel('$\Delta %s  (vs.EH) $' %prop,fontsize=20, labelpad=5)
    plt.savefig('violinplots/%s_red_diff_box.png' %prop); plt.close()
  except linalg.linalg.LinAlgError:
    print "Singular matrix on %s" %prop

names=['EH', 'EHopt', 'Aopt', 'rAopt', 'rA.006', 'rA.01', 'rA.02', 'rA.04', 'rA.08', 'rA.15', 'rA.3', 'rA.5', 'A.006', 'A.01', 'A.02', 'A.04', 'A.08', 'A.15', 'A.3', 'A.5']
names_red=['EH', 'EH_weight_opt', 'Amber_weight_opt', 'Amber_wxc_sc 0.02', 'Amber_wxc_sc 0.04']
#~ print "violinplots"
#~ for prop in cols:
  #~ if prop == 'Reso': continue
  #~ violinplot(prop)
#~ violinplot('Rgap')  


#scatter plots
def scatterplot(prop,refinex, refiney):
  if prop == 'Rgap':
    d= d_rgap.T
  else:
    d = data[:, cols.index(prop), :].T
  x = d[:, rows.index(refinex)]
  y = d[:, rows.index(refiney)]
  plt.scatter(x,y)
  if min(x) > min(y): minc= min(y)
  else: minc = min(x)
  if max(x) > max(y): maxc = max(x)
  else: maxc = max(y)
  plt.plot([minc,maxc], [minc,maxc], c='r', linewidth=1)
  plt.xlabel(refinex, fontsize=25, labelpad=0)
  plt.ylabel(refiney, fontsize=30)
  #~ plt.title(prop, fontsize=30)
  plt.tick_params(axis='both', which='major', labelsize=20)
  #~ plt.show()
  plt.savefig("scatterplots/%s_%s_%s.jpg" %(prop, refinex, refiney))
  plt.close()

for prop in cols:
  if prop == "Reso": continue
  for refine in ['noratio_opt', 'ratio_opt', 'noratio_0.02', 'noratio_0.04', 'noratio_0.08']:
    scatterplot(prop, 'EH', refine)
    scatterplot('Rgap', 'EH', refine)
  for refine in ['noratio_opt', 'ratio_opt', 'noratio_0.02', 'noratio_0.04', 'noratio_0.08']:
    scatterplot(prop, 'EH_opt', refine)    
    scatterplot('Rgap', 'EH_opt', refine)
    
# timing
def get_times_ratios(refine1, refine2):
  t1, t2, atms = [],[], []
  for pdb in pdbs:
    with open("%s/%s_001.log" %(pdb, refine1)) as f:
      f.seek(-250,2)
      for line in f.readlines():
        if "wall clock time" in line:
          t = line.split()[-2]
          t1.append(float(t))
    with open("%s/%s_001.log" %(pdb, refine2)) as f:
      f.seek(-250,2)
      for line in f.readlines():
        if "wall clock time" in line:
          t = line.split()[-2]
          t2.append(float(t))
    with open("%s/asu.rst7" %pdb) as f:
      f.readline()
      atms.append( float(f.readline().strip()) )
  for i in range(len(t1)):
    t1[i] = t2[i]/t1[i]*100
  print "\nMean cpu time Amber/EH: %5.2f" %mean(t1)
  print "Correl(d_time, n_atoms): %5.2f\n" %corrcoef(t1, atms)[0,1]
  x=atms
  y=t1
  plt.scatter(x,y)
  #~ if min(x) > min(y): minc= min(y)
  #~ else: minc = min(x)
  #~ if max(x) > max(y): maxc = max(x)
  #~ else: maxc = max(y)
  #~ plt.plot([minc,maxc], [minc,maxc], c='r', linewidth=1)
  plt.xlabel("No. atoms", fontsize=30)
  plt.ylabel("cpu time (% of EH)", fontsize=30)
  #~ plt.title(prop, fontsize=30)
  plt.tick_params(axis='both', which='major', labelsize=20)
  #~ plt.show()
  plt.savefig("time_v_natoms.png")
  plt.close()
    
t = get_times_ratios('EH', 'noratio_0.02')


# import code ; code.interact(local=dict(globals(), **locals()))
