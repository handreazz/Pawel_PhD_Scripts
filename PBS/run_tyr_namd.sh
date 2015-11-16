#!/bin/bash
#
#PBS -N hpnamd1
#PBS -l nodes=1
#PBS -l walltime=24:00:00
#PBS -o hpnamd1.out
#PBS -e hpnamd1.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/ifortvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/iccvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/mkl/tools/environment/mklvarsem64t.sh
set -x



#define variables
NETDIR=$PBS_O_WORKDIR
NODEDIR="/scratch/pjanowsk/ExRun/"
MPIR=/home/pjanowsk/NAMD_2.8_Source/Linux-x86_64-g++/charmrun
EXE=/home/pjanowsk/NAMD_2.8_Source/Linux-x86_64-g++/namd2
NP=48
SimsToRun=1

# Change to my working directory
cd ${NETDIR}
mkdir -p ${NODEDIR}
cp *.inp *prmtop *rst7 *settings ${NODEDIR}
cd ${NODEDIR}

#Loop
I=1
let IM=$I-1
RunCount=0

while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
 # if [ ! -e ${NETDIR}/RunEx/Restart/md${I}.rst7 ]; then      #see if the Restart exits, if not run sim
  #  if [ ${RunCount} -eq 0 ]; then #copy restart file if to node if this is the first sim of the cycle
   #   cp ${NETDIR}/RunEx/Restart/md${IM}.rst7 .
   # fi
   $MPIR ++local +p${NP} $EXE hairpin_namd.inp > output.txt
   cp * ${NETDIR}
   let RunCount=RunCount+1   #incerment only if sim was run
 # fi

  let I=I+1     #increment always
  let IM=IM+1
done

#clean scratch
rm -r ${NODEDIR}

