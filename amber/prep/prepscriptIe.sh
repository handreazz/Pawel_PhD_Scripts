#!/bin/bash -f 

set -x



/home/pjanowsk/amber11/bin/AddToBox \
  -c Xtalx.pdb \
  -a Na.pdb \
  -na 912 \
  -P 24228 \
  -o XtalxIe.pdb \
  -X  93.272 \
  -Y   93.272 \
  -Z   131.250 \
  -al  90.0   \
  -bt 90.0  \
  -gm  120.0   \
  -RW 3.0 \
  -RP 3.0 \
  -IG 693 \
  -V 1 \
  -G 0.1
  
/home/pjanowsk/amber11/bin/AddToBox \
  -c XtalxIe.pdb \
  -a Cl.pdb \
  -na 276 \
  -P 24228 \
  -o XtalxIe.pdb \
  -X  93.272 \
  -Y   93.272 \
  -Z   131.250 \
  -al  90.0   \
  -bt 90.0  \
  -gm  120.0   \
  -RW 3.0 \
  -RP 3.0 \
  -IG 694 \
  -V 1 \
  -G 0.1
      
/home/pjanowsk/amber11/bin/AddToBox \
  -c XtalxIe.pdb \
  -a tip4pew.pdb \
  -na 25590 \
  -P 24228 \
  -o XtalxIe.pdb \
  -X  93.272 \
  -Y   93.272 \
  -Z   131.250 \
  -al  90.0   \
  -bt 90.0  \
  -gm  120.0   \
  -RW 2.0 \
  -RP 2.0 \
  -IG 695 \
  -V 1 \
  -G 0.1

cp XtalxIe.pdb XtalxIe_Orig.pdb
reduce -trim XtalxIe.pdb >tmp.pdb 2>trim.err
grep -v "ATOM.........EPW" tmp.pdb > XtalxIeNoH.pdb

# Prepare coordinates for xtal simulation 
cat > rnatleap << EOF
source leaprc.ff99bsc0
loadoff RNA_CI.lib
loadamberparams frcmod.ionsjc_tip4pew
loadOff ions08.lib

WAT = T4E
HOH = T4E
loadAmberParams frcmod.tip4pew

loadAmberPrep so4.prepin
loadAmberParams frcmod.so4

loadoff CON.off
loadamberparams CoNH33.frcmod 

loadAmberPrep CAC.prepin
loadAmberParams frcmod.CAC0

x = loadPdb "XtalxIeNoH.pdb"
setBox x vdw 10.0
saveAmberParm x XtalxIe.top XtalxIe.crd
quit
EOF

tleap -f rnatleap > tleap_XtalxIe.out
ambpdb -p XtalxIe.top < XtalxIe.crd > XtalxIe.pdb

# Set the unit cell dimensions
/casegroup/u2/cerutti/CPrograms/ChBox \
  -c XtalxIe.crd \
  -o XtalxIe.crd \
  -X  93.272 \
  -Y  93.272 \
  -Z  131.250 \
  -al  90.0   \
  -bt  90.0  \
  -gm  120.0
