#!/bin/bash -f 

# Prepare the PDB file
/casegroup/u2/cerutti/CPrograms/UnitCell \
  -p 1BKVmod.pdb \
  -o 1BKVx.pdb 
/casegroup/u2/cerutti/CPrograms/PropPDB \
  -p 1BKVx.pdb \
  -o 1BKVx3.pdb \
  -X 117.090 \
  -Y  15.629 \
  -Z  39.715 \
  -a  90.00  \
  -b 104.46  \
  -g  90.00  \
  -ix 1      \
  -iy 3      \
  -iz 1

# Protonate the crystal
cat > protonate.tleap << EOF
source leaprc.ff99SB_spce
spceparams = loadAmberParams frcmod.spce
x = loadPdb "1BKVx3.pdb"
setBox x vdw 10.0
saveAmberParm x Xtal3x.top Xtal3x.crd
quit
EOF
$TLEAP -f protonate.tleap > protonate.out

# Set the unit cell dimensions
/casegroup/u2/cerutti/CPrograms/ChBox \
  -c Xtal3x.crd \
  -o Xtal3x.crd \
  -X  117.090 \
  -Y   46.887 \
  -Z   39.715 \
  -al  90.0   \
  -bt 104.46  \
  -gm  90.0

# Start adding solvent: biggest molecules first, trace compounds next,
# water last
$AMBPDB -p Xtal3x.top < Xtal3x.crd > Xtal3x.pdb
/casegroup/u2/cerutti/CPrograms/AddToBox \
  -c Xtal3x.pdb \
  -a Acetate.pdb \
  -na 18 \
  -P 13224 \
  -o Solv3x.pdb \
  -X  117.090 \
  -Y   46.887 \
  -Z   39.715 \
  -al  90.0   \
  -bt 104.46  \
  -gm  90.0   \
  -RW 8.0 \
  -RP 3.0 \
  -IG 691 \
  -V 1 \
  -G 0.2

/casegroup/u2/cerutti/CPrograms/AddToBox \
  -c Solv3x.pdb \
  -a chloride.pdb \
  -na 18 \
  -P 13224 \
  -o Solv3x.pdb \
  -X  117.090 \
  -Y   46.887 \
  -Z   39.715 \
  -al  90.0   \
  -bt 104.46  \
  -gm  90.0   \
  -RW 8.0 \
  -RP 3.0 \
  -IG 982 \
  -V 1 \
  -G 0.1

/casegroup/u2/cerutti/CPrograms/AddToBox \
  -c Solv3x.pdb \
  -a water.pdb \
  -na 2024 \
  -P 13224 \
  -o Solv3x.pdb \
  -X  117.090 \
  -Y   46.887 \
  -Z   39.715 \
  -al  90.0   \
  -bt 104.46  \
  -gm  90.0   \
  -RW 1.5 \
  -RP 2.0 \
  -IG 193 \
  -V 1 \
  -G 0.1

cp Solv3x.pdb Solv3xOrig.pdb

# ambpdb does not cooperate with tleap when naming hydrogens in its output
# PDB files.  So, extract just the heavy atoms and let TLEAP re-protonate
# everything
grep -v "ATOM.........H" Solv3x.pdb > tmp1
grep -v "ATOM..................1098" tmp1 > tmp2
grep -v "ATOM..................1320" tmp2 > tmp3
grep -v "ATOM..................1542" tmp3 > tmp4
grep -v "ATOM..................1764" tmp4 > tmp5
grep -v "ATOM..................1986" tmp5 > tmp6
grep -v "ATOM..................2208" tmp6 > Solv3xNoH.pdb

# Prepare coordinates for xtal simulation 
cat > build.tleap << EOF
source leaprc.ff99SB_spce
spceparams = loadAmberParams frcmod.spce
loadAmberPrep /home/cerutti/Sim1AHO/Prp/Acetate.prp
x = loadPdb "Solv3xNoH.pdb"
setbox x vdw 10.0
saveAmberParm x Solv3x.top Solv3x.crd
quit
EOF
${TLEAP} -f build.tleap > build.out
${AMBPDB} -p Solv3x.top < Solv3x.crd > Solv3x.pdb

# Set the unit cell dimensions
/casegroup/u2/cerutti/CPrograms/ChBox \
  -c Solv3x.crd \
  -o Solv3x.crd \
  -X  117.090 \
  -Y   46.887 \
  -Z   39.715 \
  -al  90.0   \
  -bt 104.46  \
  -gm  90.0

# Minimize the system
cat > minsolv.in << EOF
Initial minimization
 &cntrl
  ntx    = 1,       irest  = 0,       ntrx   = 1,      ntxo   = 1,
  ntpr   = 20,      ntwx   = 0,       ntwv   = 0,      ntwe   = 0,

  ntf    = 1,       ntb    = 1,
  cut    = 9.0,     nsnb   = 10,

  ibelly = 0,       ntr    = 1,

  imin   = 1,
  maxcyc = 1000,
  ncyc   = 100,
  ntmin  = 1,       dx0    = 0.1,     dxm    = 0.5,     drms   = 0.0001,

  ntc    = 1,       tol    = 0.00001,

 &end
Hold protein fixed
256.0
FIND
* * M *
* * S *
* * B *
* * 3 *
* O2 * *
* O * *
SEARCH
RES   1 1068
END
Hold crystal waters fixed
32.0
FIND
* * M *
* * S *
* * B *
* * 3 *
* O2 * *
* OW * *
SEARCH
RES   1069 2400
END
END
EOF

cat > minpro.in << EOG
Initial minimization
 &cntrl
  ntx    = 1,       irest  = 0,       ntrx   = 1,      ntxo   = 1,
  ntpr   = 20,      ntwx   = 0,       ntwv   = 0,      ntwe   = 0,

  ntf    = 1,       ntb    = 1,
  cut    = 9.0,     nsnb   = 10,

  ibelly = 0,       ntr    = 1,

  imin   = 1,
  maxcyc = 1000,
  ncyc   = 100,
  ntmin  = 1,       dx0    = 0.1,     dxm    = 0.5,     drms   = 0.0001,

  ntc    = 1,       tol    = 0.00001,

 &end
Restrain solvent
256.0
FIND
* * M *
* * S *
* * B *
* * 3 *
* O2 * *
* O * *
SEARCH
RES  1069 4235
END
END
EOG

cat > minall.in << EOH
Initial minimization
 &cntrl
  ntx    = 1,       irest  = 0,       ntrx   = 1,      ntxo   = 1,
  ntpr   = 20,      ntwx   = 0,       ntwv   = 0,      ntwe   = 0,

  ntf    = 1,       ntb    = 1,
  cut    = 9.0,     nsnb   = 10,

  ibelly = 0,       ntr    = 0,

  imin   = 1,
  maxcyc = 1000,
  ncyc   = 100,
  ntmin  = 1,       dx0    = 0.1,     dxm    = 0.5,     drms   = 0.0001,

  ntc    = 1,       tol    = 0.00001,

 &end
EOH

lamboot

mpirun -np 4 ${PMEMD} -O \
  -i   minsolv.in \
  -o   minsolv.out \
  -c   Solv3x.crd \
  -p   Solv3x.top \
  -ref Solv3x.crd \
  -r   Solv3x.minsolv < /dev/null

mpirun -np 4 ${PMEMD} -O \
  -i   minpro.in \
  -o   minpro.out \
  -c   Solv3x.minsolv \
  -p   Solv3x.top \
  -ref Solv3x.minsolv \
  -r   Solv3x.minpro < /dev/null

mpirun -np 4 ${PMEMD} -O \
  -i   minall.in \
  -o   minall.out \
  -c   Solv3x.minpro \
  -p   Solv3x.top \
  -ref Solv3x.minpro \
  -r   Solv3x.minall < /dev/null

lamhalt
