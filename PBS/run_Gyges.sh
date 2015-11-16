#!/bin/bash
#
#PBS -N RedRun
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o RedRun.out
#PBS -e RedRun.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x

#define variables
NETDIR=$PBS_O_WORKDIR
EQFILE=equilibrate/RedWaterPep_Eq9.rst7
NODEDIR="/scratch/pjanowsk/RedRun/"
TOPO=RedWaterPep.prmtop
NP=8
SimsToRun=8

# Change to my working directory
cd ${NETDIR}

# Create subdirectories and prepare restart file
mkdir -p RunRed/Restart/ RunRed/Energy/ RunRed/Trajectory/ RunRed/Out/
if [ ! -e RunRed/Restart/md0.rst7 ]; then
  cp ${EQFILE} RunRed/Restart/md0.rst7
fi

# Create a directory on the node scratch disk for our work and copy topo
mkdir -p ${NODEDIR}
cp $TOPO ${NODEDIR}
cd ${NODEDIR}



#Loop
I=1
let IM=$I-1
RunCount=0



cat > md.in << EOF
Standard MD run input
 &cntrl

  nmropt = 0,
  ntx    = 5,       irest  = 1,
  ntrx   = 1,       ntxo   = 1,
  ntpr   = 10000,   ntwx   = 10000,
  ntwv   = -1,       ntwe   = 10000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = 2,
  es_cutoff   =  8.0,
  vdw_cutoff  = 12.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 1000000,
  nscm   = 10000,
  t      = 0.0,     dt     = 0.002,

  temp0     = 277.0,   tempi  = 277.0,
  ig        = -1,
  ntt       = 2,

  ntp    = 1,       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
EOF


while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
  if [ ! -e ${NETDIR}/RunRed/Restart/md${I}.rst7 ]; then      #see if the Restart exits, if not run sim
    if [ ${RunCount} -eq 0 ]; then #copy restart file if to node if this is the first sim of the cycle
      cp ${NETDIR}/RunRed/Restart/md${IM}.rst7 .
    fi
    mpirun -np 8 pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p ${TOPO} \
          -c md${IM}.rst7 \
          -r md${I}.rst7 \
          -x md${I}.nc \
          -e md${I}.en
    cp md${I}.rst7 ${NETDIR}/RunRed/Restart/
    mv md${I}.out ${NETDIR}/RunRed/Out/
    mv md${I}.nc ${NETDIR}/RunRed/Trajectory/
    mv md${I}.en ${NETDIR}/RunRed/Energy/
    let RunCount=RunCount+1   #incerment only if sim was run
  fi

  let I=I+1     #increment always
  let IM=IM+1
done

#clean scratch
rm -r ${NODEDIR}

