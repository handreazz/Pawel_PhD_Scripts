import os, sys
import subprocess
import matplotlib.pyplot as plt
from numpy import *
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import re
sns.set_style("whitegrid")

# Plot bar graphs of select set of pdb codes on two side by side bar graphs.

palettes=['pastel', 'bold', 'muted', 'deep', 'dark', 'colorblind',
          'husl', 'hls']


cp = sns.dark_palette('Bisque', 4)
cp = sns.color_palette(palettes[4],10)



def plot_rfree(codes, ax):
  noafitt = []
  afitt = []
  for code in codes:
    with open('%s/%s_no_afitt___001.log' %(code,code)) as f:
      rfree=f.readlines()[-1].strip().split()[-1]
      noafitt.append(float(rfree))
    with open('%s/%s_sc_10_adp__001.log' %(code,code)) as f:
      rfree=f.readlines()[-1].strip().split()[-1]
      afitt.append(float(rfree))


  width=0.20
  x = arange(len(codes))
  b1 = ax.bar(x+width*.5, noafitt,width, color=cp[1])
  b2 = ax.bar(x+width*1.5, afitt,width, color=cp[3])


  ax.set_ylabel('R-free', fontsize=36)
  ax.set_xticks(x+width)
  labels=[code for code in codes]
  ax.set_xticklabels( labels )
  ax.tick_params(axis='both', labelsize=20)
  ax.set_xticklabels( labels, fontsize=16 )
  ax.legend( (b1[0], b2[0]), ('AFITT-cif', 'PHENIX-AFITT'), fontsize=20 )
  # plt.show()
  # plt.savefig('rfree_afitt_EH.png')



def plot_energies(codes,scales, ax):
  noafitt = []
  afitt = []
  deposited = []
  buster = []
  pattern1=re.compile(r'sc_sc_10_adp_')
  pattern2=re.compile(r'sc_no_afitt__')
  labels=[]

  for code in codes:
    with open('%s/%s_energy.dat' %(code,code)) as f:
      lines = f.readlines()
      ligands=[ligand for ligand in lines[0].strip().split()]
      dep_ene = [ene for ene in lines[1].strip().split()]
      for ene in dep_ene[1:]:
        deposited.append(float(ene))
      for ligand in range(len(ligands)):
        for line in lines:
          if re.search(pattern1, line):
            afitt.append(float(line.split()[ligand+1]))
            labels.append('%s_%s' %(code,ligands[ligand][:-1].split('_')[0]))
            break
          elif re.search(pattern2, line):
            noafitt.append(float(line.split()[ligand+1]))

  afitt = [a/b*100 for a,b in zip(afitt,deposited)]
  noafitt =  [a/b*100 for a,b in zip(noafitt,deposited)]

  width=0.20
  x = arange(len(afitt))
  # b1 = ax.bar(x,       deposited, width, color=cp[0])
  b2 = ax.bar(x+width*.5,noafitt, width, color=cp[1])
  b3 = ax.bar(x+width*1, afitt,   width, color=cp[2])

  ax.set_ylabel('Energy (kJ/mol', fontsize=34)
  ax.set_ylabel('Energy (% of PDB deposited)', fontsize=34)
  ax.tick_params(axis='both', labelsize=20)
  ax.set_xticks(x+width)
  ax.set_xticklabels( labels, fontsize=14 )
  ax.set_xlim(-.2)
  ax.legend( (b2[0], b3[0]),
             ('AFITT-cif', 'PHENIX-AFITT'), fontsize=20 )
  # plt.show()
  # plt.savefig('energy_afitt_EH.png')



#======================================================================#

scales=[5,7,10,12,15,17,20,40,80]
codes=['1fjs', '1ctr', '1fbl', '1gwx', '2tmn', '1l7f', '1ydt', '1cvu']
buster_codes=['1cvu','1fjs', '1gwx','1l7f','1ydt','1fq5']


fig=plt.figure(figsize=(24, 12))
fig.subplots_adjust(wspace=.15,right=.95, left=.05,top=.93, bottom=.05, hspace=.35)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# sns.set_context("poster")
plot_energies(codes,scales, ax1)
plot_rfree(codes,ax2)
# plt.show()
plt.savefig('energy_rfree_pub.tif', dpi=200)



