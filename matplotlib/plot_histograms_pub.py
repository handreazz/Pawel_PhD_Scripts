import os, sys
import matplotlib.pyplot as plt
from numpy import *
import seaborn as sns
import re
sns.set_style("whitegrid")
import pickle

# This will plot all the AFITT paper plots except fig 4 and 5
# /home/pjanowsk/c/OpenEye/afitt/Iridium_1/plot_energy_r_pub.py
# /home/pjanowsk/c/OpenEye/afitt/Phenix-AFITT_Altconf_1/plot_energy_r_pub.py

#=======================================================================
#                                  Get data
#=======================================================================
with open("pickle.dat", "rb") as f:
    data_from_pickle = pickle.load(f)
# # data not used
# en_elbo = data_from_pickle[3]
# en_10_20 = data_from_pickle[4]
# en_elbo_10 = data_from_pickle[7]
# rfree_elbo = data_from_pickle[11]
# rfree_20_noaf = data_from_pickle[13]
# rfree_10_20 = data_from_pickle[14]
# rfree_elbo_10 = data_from_pickle[15]

# ENERGIES
en_10 = data_from_pickle[0]
en_noaf = data_from_pickle[1]
en_depo = data_from_pickle[2]
en_depo_10 = data_from_pickle[5]
en_noaf_10 = data_from_pickle[6]

# RFREE
rfree_10 = data_from_pickle[8]
rfree_noaf = data_from_pickle[9]
rfree_depo = data_from_pickle[10]
rfree_noaf_10 = data_from_pickle[12]

# TIMES
times_noaf = data_from_pickle[16]
times_10 = data_from_pickle[17]
times_noaf_10 = data_from_pickle[18]

# MOGUL
mogul_bond_depo = data_from_pickle[19]
mogul_bond_noaf = data_from_pickle[20]
mogul_bond_10   = data_from_pickle[21]
mogul_ang_depo  = data_from_pickle[22]
mogul_ang_noaf  = data_from_pickle[23]
mogul_ang_10    = data_from_pickle[24]

#=======================================================================
#                                Plot functions
#=======================================================================

#////////////////////////////#
# ENERGY HISTOGRAM & SCATTER #
#////////////////////////////#

fig=plt.figure(figsize=(24, 12))

#Left plot
ax1 = fig.add_subplot(121)
#Plot data
l1 = sns.distplot(en_10,   label = 'Phenix-AFITT  %5.2f' %mean(en_10), norm_hist=False)
l2 = sns.distplot(en_noaf, label = 'AFITT-cif     %5.2f' %mean(en_noaf), norm_hist=False)
l3 = sns.distplot(en_depo, label = 'PDB           %5.2f' %mean(en_depo), norm_hist=False)
#Axis labels and ticks
plt.xlim(xmax=1000)
ax1.set_xlabel('Energy $(kJ/mol)$', fontsize=28)
ax1.set_ylabel('Normalized distribution', fontsize=28, labelpad=0)
ax1.tick_params(axis='both', labelsize=24)
for t in ax1.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
ax1.set_yticklabels([], minor=False)
for spine in ax1.spines.values():
  spine.set_linewidth(2)
  spine.set_color('k')

#Legend
legend = ax1.legend(prop={'size':20, 'family':'monospace'}, frameon=True,
                    bbox_to_anchor=(0.98, 0.75),
                    title='                                       Mean')
legend.get_frame().set_edgecolor('k')
legend.get_frame().set_linewidth(1.0)
legend.get_title().set_fontsize('18')

#Right plot
ax2 = fig.add_subplot(122)
ax2.scatter(en_depo, en_10, c='b', label='PDB       +%d%% '%mean(en_depo_10), s=40, lw=0)
ax2.scatter(en_noaf, en_10, c='r', label='AFITT-cif +%d%% '%mean(en_noaf_10), s=40, lw=0)
#Diagonal line
minc = min([min(en_depo), min(en_noaf), min(en_10)])
maxc = max([max(en_depo), max(en_noaf), max(en_10)])
maxc =maxc*1.05
plt.plot([minc,maxc], [minc,maxc], c='k', linewidth=1)
#Axis labels and ticks
plt.xlim((0,maxc))
plt.ylim((0,maxc))
ax2.set_xlabel('Energy PDB($blue$) & AFITT-cif($red$)  $(kJ/mol)$', fontsize=28)
ax2.set_ylabel('Energy Phenix-AFITT  $(kJ/mol)$', fontsize=28, labelpad=1)
ax2.tick_params(axis='both', labelsize=24)
for spine in ax2.spines.values():
  spine.set_linewidth(2)
  spine.set_color('k')
#Legend
legend = ax2.legend(prop={'size':20, 'family':'monospace'},
                    bbox_to_anchor=(0.4, 0.9), frameon=True,
                    title = '                                 $<\Delta E>$ vs.\n'
                            '                               Phenix-AFITT')
legend.get_title().set_fontsize('20')
legend.get_frame().set_edgecolor('k')
legend.get_frame().set_linewidth(1.0)
legend.get_title().set_fontsize('16')

#Tight border
fig.tight_layout()

# #Draw plot borders
# rec1 = plt.Rectangle((-40,-.0003),1073, .00435,
#                     fill=False,lw=2)
# rec1 = ax1.add_patch(rec1)
# rec1.set_clip_on(False)
# rec2 = plt.Rectangle((1033,-.0003),1108, .00435,
#                     fill=False,lw=2)
# rec2 = ax1.add_patch(rec2)
# rec2.set_clip_on(False)

# plt.show()
# plt.savefig("Ene_hist_scat_pub.eps")
plt.savefig("Ene_hist_scat_pub.tif", dpi=200)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#////////////////////////////#
# R-FREE HISTOGRAM           #
#////////////////////////////#

fig=plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(111)
cmap = sns.color_palette()
#Plot data
l1 = sns.distplot(rfree_10,
                  label = 'Phenix-AFITT  %5.3f' %mean(rfree_10),
                  color = cmap[0], kde_kws={"lw": 3})
l2 = sns.distplot(rfree_noaf,
                  label = 'AFITT-cif     %5.3f' %mean(rfree_noaf),
                  color = cmap[2], kde_kws={"lw": 3})
#Axis labels and ticks
plt.xlim((0.1, 0.4))
ax1.set_xlabel('R-free', fontsize=28)
ax1.set_ylabel('Normalized distribution', fontsize=28, labelpad=0)
ax1.tick_params(axis='both', labelsize=24)
for t in ax1.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
# ax1.set_yticklabels([], minor=False)
#Legend
legend = ax1.legend(prop={'size':20, 'family':'monospace'}, frameon=True,
                    bbox_to_anchor=(0.98, 0.75),
                    title='                                       Mean')
legend.get_frame().set_edgecolor('k')
legend.get_frame().set_linewidth(1.0)
legend.get_title().set_fontsize('18')
fig.tight_layout()

# plt.show()
plt.savefig("Rfree_hist_pub.tif", dpi=200)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#////////////////////////////#
# TIMINGS HISTOGRAM          #
#////////////////////////////#

fig=plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
cmap = sns.color_palette()

#Plot data
l1 = sns.distplot(times_noaf_10,color = "k")

#Axis labels and ticks
plt.xlim((-100, 100))
ax.set_xlabel('$\Delta$ Time $(\%)$', fontsize=28)
ax.set_ylabel('Normalized distribution', fontsize=28, labelpad=10)
ax.tick_params(axis='both', labelsize=24)
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
#Text box
textstr="mean = %5.2f" %(mean(times_noaf_10))
props = dict(boxstyle='square', facecolor='white', edgecolor='k', linewidth=1)
t = ax.text(0.10, 0.95, textstr, transform=ax.transAxes, fontsize=24,
      verticalalignment='top', bbox=props)
fig.tight_layout()
# plt.show()
plt.savefig("Timing_hist_pub.tif", dpi=200)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

#////////////////////////////#
# MOGUL_HISTOGRAMS           #
#////////////////////////////#

cmap = sns.color_palette()

pdb_b = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/pdb_bonds.dat')
noaf_b = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/noafit_bonds.dat')
afit_b = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/afit_bonds.dat')

pdb_a = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/pdb_angles.dat')
noaf_a = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/noafit_angles.dat')
afit_a = genfromtxt('/home/pjanowsk/c/OpenEye/afitt/mogul/all/afit_angles.dat')



fig=plt.figure(figsize=(16, 8))

# Top plot
ax1 = fig.add_subplot(211)

#Plot data
l1 = sns.distplot(afit_b[0:281]*100,  label = 'PHENIX-AFITT', hist=False, norm_hist=True, color=cmap[0])
l2 = sns.distplot(noaf_b[0:281]*100,   label = 'AFITT CIF', hist=False, norm_hist=True, color=cmap[1])
l3 = sns.distplot(pdb_b[0:281]*100,   label = 'PDB', hist=False,  norm_hist=True, color=cmap[2])

ax1.plot([median(afit_b)*100, median(afit_b)*100], [0, 0.532], color=cmap[0], ls='--')
ax1.plot([median(noaf_b)*100, median(noaf_b)*100], [0, 0.752], color=cmap[1], ls='--')
ax1.plot([median(pdb_b)*100, median(pdb_b)*100], [0, 0.233], color=cmap[2], ls='--')




# num_bins = 50
# the histogram of the data
# n, bins, patches = ax1.hist(pdb_b*100, 20, histtype='step', linewidth=3)
# n, bins, patches = ax1.hist(noaf_b*100, 20, histtype='step', linewidth=3)
# n, bins, patches = ax1.hist(afit_b*100, 20, histtype='step', linewidth=3)

#Axis labels and ticks
plt.xlim((0,8))
ax1.set_xlabel('Bond RMSD $(\AA)$', fontsize=20)
ax1.tick_params(axis='both', labelsize=18)
for spine in ax1.spines.values():
  spine.set_linewidth(2)
  spine.set_color('k')
ax1.set_xticklabels([0,.01,.02,.03,.04,.05,.06,.07,.08])


# Bottom plot
ax2 = fig.add_subplot(212)

#Plot data
l4 = sns.distplot(afit_a,   label = 'afit', hist=False, norm_hist=True)
l5 = sns.distplot(noaf_a,   label = 'noaf', hist=False, norm_hist=True)
l6 = sns.distplot(pdb_a,   label = 'pdb', hist=False, norm_hist=True)

ax2.plot([median(afit_a), median(afit_a)], [0, 0.68], color=cmap[0], ls='--')
ax2.plot([median(noaf_a), median(noaf_a)], [0, 0.57], color=cmap[1], ls='--')
ax2.plot([median(pdb_a), median(pdb_a)], [0, 0.3], color=cmap[2], ls='--')

# Axis labels and ticks
plt.xlim((0,8))
#plt.ylim((0,400))
ax2.set_xlabel('Angle RMSD $(\deg)$', fontsize=20)
ax2.tick_params(axis='both', labelsize=20)
for spine in ax2.spines.values():
  spine.set_linewidth(2)
  spine.set_color('k')


#Legend
legend = ax1.legend(prop={'size':18, 'family':'monospace'},
                    bbox_to_anchor=(0.9, 0.9), frameon=True)
# legend.get_frame().set_edgecolor('k')
# legend.get_frame().set_linewidth(1.0)

leg=ax2.legend([])
leg.remove()
#Tight border
fig.tight_layout()

#Draw plot borders
# rec1 = plt.Rectangle((-40,-.0003),1073, .00435,
#                     fill=False,lw=2)
# rec1 = ax1.add_patch(rec1)
# rec1.set_clip_on(False)
# rec2 = plt.Rectangle((1033,-.0003),1108, .00435,
#                     fill=False,lw=2)
# rec2 = ax1.add_patch(rec2)
# rec2.set_clip_on(False)

# plt.show()
plt.savefig("Mogul_pub.tif", dpi=300)