#!/bin/bash
#
#PBS -N 1rpgKeq
#PBS -l nodes=1
#PBS -l walltime=24:00:00
#PBS -o 1rpgKeq.out
#PBS -e 1rpgKeq.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/ifortvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/iccvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/mkl/tools/environment/mklvarsem64t.sh
set -x



#define variables
NETDIR=$PBS_O_WORKDIR
MPIR=/home/pjanowsk/NAMD_2.8_Source/Linux-x86_64-g++/charmrun
EXE=/home/pjanowsk/NAMD_2.8_Source/Linux-x86_64-g++/namd2
NP=48
SimsToRun=2
TOPO=1rpgK.prmtop
COOR=1rpgK.rst7

# Change to my working directory
cd ${NETDIR}

#Loop
I=1
let IM=$I-1
RunCount=0

while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
  if [ ! -e md${I}.coor ]; then      #see if the Restart exits, if not run sim

# CREATE INPUT
cat > namd.in << EOF
#############################################################
## 							   ##
##   ADD THE DESCRIPTION HERE !!!!!                        ##
##                                                         ##
#############################################################

source ./namd_data/OUT.settings
source ./namd_data/NPT.settings
source ./namd_data/PME.settings

#############################################################
## OUTPUT/INPUT                                            ##
#############################################################

parmfile ${TOPO}
ambercoor ${COOR}

bincoordinates md${IM}.coor 
binvelocities  md${IM}.vel
extendedSystem md${IM}.xsc

outputName     md${I}


#############################################################
## EXECUTION SCRIPT                                        ##
#############################################################

run 5000000
EOF

   #RUN SIMULATION
$MPIR ++local +p${NP} $EXE namd.in > md${I}.out

   let RunCount=RunCount+1   		#incerment only if sim was run
  fi

  let I=I+1     			#increment always
  let IM=IM+1
done
