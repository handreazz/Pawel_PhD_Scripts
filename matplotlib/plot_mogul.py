import os, sys
import matplotlib.pyplot as plt
from numpy import *
import seaborn as sns
sns.set_style("whitegrid")
cmap = sns.color_palette()

pdb_b = genfromtxt('pdb_bonds.dat')
noaf_b = genfromtxt('noafit_bonds.dat')
afit_b = genfromtxt('afit_bonds.dat')

pdb_a = genfromtxt('pdb_angles.dat')
noaf_a = genfromtxt('noafit_angles.dat')
afit_a = genfromtxt('afit_angles.dat')



fig=plt.figure(figsize=(16, 8))

# Top plot
ax1 = fig.add_subplot(211)

#Plot data
l1 = sns.distplot(afit_b[0:281]*100,  label = 'PHENIX-AFITT', hist=False, norm_hist=True, color=cmap[0])
l2 = sns.distplot(noaf_b[0:281]*100,   label = 'AFITT cif', hist=False, norm_hist=True, color=cmap[1])
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
plt.savefig("Mogul_pub.png")