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

# Change to my working directory
cd ${NETDIR}
$MPIR ++local +p${NP} $EXE min1.in > min1.out
$MPIR ++local +p${NP} $EXE min2.in > min2.out

cp min2.coor md0.coor 
cp min2.vel md0.vel
cp min2.xsc md0.xsc 
