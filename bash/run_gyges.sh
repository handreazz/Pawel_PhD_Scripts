#!/bin/bash
#
#PBS -N ExRun
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o ExRun.out
#PBS -e ExRun.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea


set -x

#define variables
NETDIR=$PBS_O_WORKDIR
EQFILE=/net/casegroup2/u2/pjanowsk/Case/4lzt/equilibration/tyr_Sa/Eq9.rst7
NODEDIR="/scratch/pjanowsk/SaRun/"
TOPO=4lztSa.prmtop
NP=8
SimsToRun=10
EXE=pmemd.MPI
MPIR=mpirun

# Change to my working directory
cd ${NETDIR}

# Create subdirectories and prepare restart file
mkdir -p RunEx/Restart/ RunEx/Energy/ RunEx/Trajectory/ RunEx/Out/
if [ ! -e RunEx/Restart/md0.rst7 ]; then
  cp ${EQFILE} RunEx/Restart/md0.rst7
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
  ntwv   = 0,       ntwe   = 0,   ntwr=0,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = 2,
  es_cutoff   =  9.0,
  vdw_cutoff  =  9.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 1000000,
  nscm   = 10000,
  t      = 0.0,     dt     = 0.002,

  temp0     = 295.0,   tempi  = 295.0,
  ntt       = 3,  gamma_ln = 1.0, ig = -1,

  ntp    = 1,       pres0  = 1.0,     comp   = 44.6,
  taup   = 5.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
EOF


while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
  if [ ! -e ${NETDIR}/RunEx/Restart/md${I}.rst7 ]; then      #see if the Restart exits, if not run sim
    if [ ${RunCount} -eq 0 ]; then #copy restart file if to node if this is the first sim of the cycle
      cp ${NETDIR}/RunEx/Restart/md${IM}.rst7 .
    fi
    $MPIR -np $NP $EXE -O \
          -i md.in \
          -o md${I}.out \
          -p ${TOPO} \
          -c md${IM}.rst7 \
          -r md${I}.rst7 \
          -x md${I}.nc \
          -e md${I}.en
    cp md${I}.rst7 ${NETDIR}/RunEx/Restart/
    mv md${I}.out ${NETDIR}/RunEx/Out/
    mv md${I}.nc ${NETDIR}/RunEx/Trajectory/
    mv md${I}.en ${NETDIR}/RunEx/Energy/
    let RunCount=RunCount+1   #incerment only if sim was run
  fi

  let I=I+1     #increment always
  let IM=IM+1
done

#clean scratch
rm -r ${NODEDIR}

