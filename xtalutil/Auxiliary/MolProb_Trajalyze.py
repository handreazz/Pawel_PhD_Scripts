#! /usr/bin/env python
import os
import sys
import commands
from numpy import *

#======================================================================#
#                                                                      #
# Obtain molprobity statistics for an entire crystal MD trajectory.    #
# This script uses the phenix molprobity scripts so make sure phenix   #
# is installed and up-to-date.                                         #
#                                                                      #
# Variables (set by hand below):                                       #
#   UC: no. of unit cells in the crystal supercell                     #
#   ASU: no. of asymmetric units per unit cell                         #
#   revsym_path: path to the "reverse symmetry" unit cell trajectories #
#             These are usually built by the "RevSym_netcdf.py" script.#
#   cryst1: CRYST1 record for the unit cell (usually obtained from the #
#           PDB file.                                                  #
#   frames_sk: analyze trajectory every this many frames               #
#                                                                      #
# Output:                                                              #
#   The script will create the following text files. Rows correspond to#
#   frames and columns correspond to successive asymmetric units.      #
#   clash_array - molprobity clash score (the number of all-atom       #
#                     steric overlaps > 0.4A per 1000 atoms.           #
#   rotout_array - percent of rotamer outliers                         #
#   ramout_array - percent of ramachandran plot outliers               #
#   ramfav_array - percent of favorable ramachandran plot points       #
#   cbdev_array  - number of C-beta outliers                           #
#   mpr_score    - molprobity score(see code for formula)              #
#======================================================================#

##############
# USER SETUP #
##############
UC=12
ASU=1
revsym_path="../1.5ms_analysis/revsym/"
cryst1="CRYST1   27.245   31.875   34.236  88.52 108.53 111.89 P 1           1"
frames_sk=20



#======================================================================#
#======================================================================#

# get number of frames in trajectory
frames_f=int(commands.getoutput('ncframes %s/RevSym_01_01.nc' %revsym_path))


# initialize data arrays
frames_tot=int((frames_f-0.5)/frames_sk)+1  #number of frames after skipping
clash_array=zeros((frames_tot,UC*ASU))
ramfav_array=zeros((frames_tot,UC*ASU))
ramout_array=zeros((frames_tot,UC*ASU))
cbdev_array=zeros((frames_tot,UC*ASU))
rotout_array=zeros((frames_tot,UC*ASU))
mpr_score=zeros((frames_tot,UC*ASU))


for frame in range(0,frames_f,frames_sk):
	for i in range(UC):
		for j in range(ASU):
			
			# use cpptraj to get pdb file of frame
			f=open('ctraj_getframe','w')
			f.write('parm ../4lztUC.prmtop\n')
			f.write('trajin %s/RevSym_%02d_%02d.nc %d %d 1\n ' %(revsym_path,i+1,j+1,frame+1,frame+1))
			f.write('trajout frame1.pdb pdb\n')
			f.close()
			os.system('cpptraj -i ctraj_getframe >/dev/null')
			
			#rename Amber-specific residues and add CRYST1
			os.system('echo "%s" | cat - frame1.pdb > frame2.pdb' %cryst1)
			os.system('sed -i "s/CYX/CYS/g" frame2.pdb')
			os.system('sed -i "s/HID/HIS/g" frame2.pdb')
			os.system('sed -i "s/HIE/HIS/g" frame2.pdb')
			os.system('sed -i "s/HIP/HIS/g" frame2.pdb')
			os.system('phenix.reduce -trim frame2.pdb >frame3.pdb 2>/dev/null')
			os.system('phenix.reduce frame3.pdb >frame4.pdb 2>/dev/null')

			#run phenix molprobity and parse output for statistic
			x=commands.getoutput('phenix.clashscore frame4.pdb')
			clash=float(x.splitlines()[-1].split()[-1])
			x=commands.getoutput('phenix.ramalyze frame4.pdb')
			ramout= float(x.splitlines()[-2].split()[1][0:-1])
			ramfav=float(x.splitlines()[-1].split()[1][0:-1])
			x=commands.getoutput('phenix.rotalyze frame4.pdb')
			rotout=float(x.splitlines()[-1].split()[1][0:-1])
			x=commands.getoutput('phenix.cbetadev frame4.pdb')
			cbdev=int(x.splitlines()[-1].split()[1])
			#~ Molprb-Score = 0.426 *ln(1 + Clash-Score) + 0.33 *ln(1 + max(0, Rot-out - 1)) + 0.25 *ln( 1 + max(0, (100 - Ram-fv) - 2 )) + 0.5
			mpr=0.426*log(1+clash)+0.33*log(1+max(0,rotout-1))+0.25*log(1+max(0,100-ramfav-2)+0.5
			

			#populate array
			clash_array[frame/frames_sk,i*ASU+j]=clash
			ramfav_array[frame/frames_sk,i*ASU+j]=ramfav
			ramout_array[frame/frames_sk,i*ASU+j]=ramout
			rotout_array[frame/frames_sk,i*ASU+j]=rotout
			cbdev_array[frame/frames_sk,i*ASU+j]=cbdev
			mpr_score[frame/frames_sk,i*ASU+j]=mpr
			
			#standard output
			print 'Frame: %d UC: %d ASU: %d' %(frame+1,i+1,j+1) 
			print 'Clashscore: %5.4f' %clash
			print 'Ramachandran favored: %4.2f%%' %ramfav
			print 'Ramachandran outliers: %4.2f%%' %ramout
			print 'Rotamer outliers: %4.2f%%' %rotout
			print 'Cbeta outliers: %d' %cbdev
			print '\n'

#save arrays
savetxt('clash_array.out', clash_array, fmt='%7.4f')
savetxt('ramfav_array.out', ramfav_array, fmt='%5.2f')
savetxt('ramout_array.out', ramout_array, fmt='%5.2f')
savetxt('rotout_array.out', rotout_array, fmt='%5.2f')
savetxt('cbdev_array.out', cbdev_array, fmt='%4d')
savetxt('mpr_score.out', mpr_score, fmt='%7.4f')

#clean up
os.system('rm frame*pdb')
