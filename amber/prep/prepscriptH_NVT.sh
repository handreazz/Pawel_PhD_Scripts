#!/bin/bash -f 

set -x



#~ cat > tleap_chimera << EOF
#~ source leaprc.ff10
#~ loadamberparams frcmod.ionsjc_tip4pew
#~ loadamberparams frcmod.tip4pew
#~ WAT = T4E
#~ HOH = T4E
#~ set default FlexibleWater on
#~ loadAmberPrep MPD.prepin
#~ x = loadpdb "tmp2.pdb"
#~ bond x.40.SG x.95.SG
#~ bond x.26.SG x.84.SG
#~ bond x.65.SG x.72.SG
#~ bond x.58.SG x.110.SG
#~ bond x.331.SG x.386.SG
#~ bond x.317.SG x.375.SG
#~ bond x.356.SG x.363.SG
#~ bond x.349.SG x.401.SG
#~ setBox x vdw 10.0
#~ saveAmberParm x 1rpgX_chimera.prmtop 1rpgX_chimera.rst7
#~ EOF
#~ tleap -f tleap_chimera > tleap_chimera.out
#~ 
#~ # Set the unit cell dimensions
#~ ChBox \
  #~ -c 1rpgX_chimera.rst7 \
  #~ -o 1rpgX_chimera.rst7 \
  #~ -X 30.000 \
  #~ -Y 38.270 \
  #~ -Z 53.170 \
  #~ -al 90.00  \
  #~ -bt 106.00 \
  #~ -gm 90.00  
  #~ 
#~ ambpdb -p 1rpgX_chimera.prmtop < 1rpgX_chimera.rst7 > 1rpgX_chimera.pdb

##AddToBox\
  ##-c 1rpgX.pdb \
  ##-a Na.pdb \
  ##-na 1 \
  ##-P 3882 \
  ##-o 1rpgH.pdb \
  ##-X 30.000 \
  ##-Y 38.270 \
  ##-Z 53.170 \
  ##-al 90.00  \
  ##-bt 106.00 \
  ##-gm 90.00  \
  ##-RW 3.0 \
  ##-RP 3.0 \
  ##-IG 693 \
  ##-V 1 \
  ##-G 0.1
  
AddToBox\
  -c 1rpgX.pdb \
  -a Cl.pdb \
  -na 14 \
  -P 3882 \
  -o 1rpgH_NVT.pdb \
  -X 30.000 \
  -Y 38.270 \
  -Z 53.170 \
  -al 90.00  \
  -bt 106.00 \
  -gm 90.00  \
  -RW 3.0 \
  -RP 3.0 \
  -IG 694 \
  -V 1 \
  -G 0.1
      
AddToBox\
  -c 1rpgH_NVT.pdb \
  -a tip4pew.pdb \
  -na 485 \
  -P 3882 \
  -o 1rpgH_NVT.pdb \
  -X 30.000 \
  -Y 38.270 \
  -Z 53.170 \
  -al 90.00  \
  -bt 106.00 \
  -gm 90.00  \
  -RW 3.0 \
  -RP 3.0 \
  -IG 695 \
  -V 1 \
  -G 0.1

cp 1rpgH_NVT.pdb 1rpgH_NVT_Orig.pdb
reduce -trim 1rpgH_NVT.pdb >tmp.pdb 2>trim.err
grep -v "ATOM.........EPW" tmp.pdb > 1rpgH_NVT_NoH.pdb

# Prepare coordinates for xtal simulation 
cat > rnatleap << EOF
source leaprc.ff10
loadamberparams frcmod.ionsjc_tip4pew
loadamberparams frcmod.tip4pew
WAT = T4E
HOH = T4E
set default FlexibleWater on
loadAmberPrep MPD.prepin
x = loadpdb "1rpgH_NVT_NoH.pdb"
bond x.40.SG x.95.SG
bond x.26.SG x.84.SG
bond x.65.SG x.72.SG
bond x.58.SG x.110.SG
bond x.331.SG x.386.SG
bond x.317.SG x.375.SG
bond x.356.SG x.363.SG
bond x.349.SG x.401.SG
setBox x vdw 10.0
saveAmberParm x 1rpgH_NVT.prmtop 1rpgH_NVT.rst7
quit
EOF

tleap -f rnatleap > tleap.out
ambpdb -p 1rpgH_NVT.prmtop < 1rpgH_NVT.rst7 > 1rpgH_NVT.pdb

# Set the unit cell dimensions
ChBox \
  -c 1rpgH_NVT.rst7 \
  -o 1rpgH_NVT.rst7 \
  -X 30.000 \
  -Y 38.270 \
  -Z 53.170 \
  -al 90.00  \
  -bt 106.00 \
  -gm 90.00

./clean_prmtop_namd.sh 1rpgH_NVT.prmtop

# Prepare coordinates for xtal simulation  AMBER
cat > rnatleap << EOF
source leaprc.ff10
loadamberparams frcmod.ionsjc_tip4pew
loadamberparams frcmod.tip4pew
WAT = T4E
HOH = T4E
loadAmberPrep MPD.prepin
x = loadpdb "1rpgH_NVT_NoH.pdb"
bond x.39.SG x.94.SG
bond x.25.SG x.83.SG
bond x.64.SG x.71.SG
bond x.57.SG x.109.SG
bond x.166.SG x.221.SG
bond x.152.SG x.210.SG
bond x.191.SG x.198.SG
bond x.184.SG x.236.SG
setBox x vdw 10.0
saveAmberParm x amb_1rpgH_NVT.prmtop amb_1rpgH_NVT.rst7
quit
EOF

tleap -f rnatleap > tleap.out
ambpdb -p amb_1rpgH_NVT.prmtop < amb_1rpgH_NVT.rst7 > amb_1rpgH_NVT.pdb

# Set the unit cell dimensions
ChBox \
  -c amb_1rpgH_NVT.rst7 \
  -o amb_1rpgH_NVT.rst7 \
  -X 30.000 \
  -Y 38.270 \
  -Z 53.170 \
  -al 90.00  \
  -bt 106.00 \
  -gm 90.00
