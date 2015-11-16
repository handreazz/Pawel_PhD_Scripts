#!/bin/bash
#
#PBS -N EXmin
#PBS -l nodes=1
#PBS -l walltime=24:00:00
#PBS -o Extyr.out
#PBS -e Extyr.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/ifortvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/iccvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/mkl/tools/environment/mklvarsem64t.sh

set -x
cd $PBS_O_WORKDIR

#EXE=/cottus/opt/amber11-dev/bin/pmemd.MPI
#EXE=pmemd.MPI
EXE=/cottus/home/pjanowsk/amber11/bin/pmemd.MPI

#MPIR=/cottus/opt/amber11-dev/bin/mpirun
MPIR=/cottus/home/pjanowsk/amber11/bin/mpirun

#/cottus/opt/amber11-dev/bin/mpirun -np 4 $EXE -O \

$MPIR -np 4 $EXE -O \
  -i   Exminsolv.in \
  -o   Exminsolv.out \
  -c   ExWaterPep.rst7 \
  -p   ExWaterPep.prmtop \
  -ref ExWaterPep.rst7 \
  -r   ExWaterPep_minsolv.rst7

#~ /cottus/opt/amber11-dev/bin/mpirun -np 4 $EXE -O \
  #~ -i   Exminpro.in \
  #~ -o   Exminpro.out \
  #~ -c   ExWaterPep_minsolv.rst7 \
  #~ -p   ExWaterPep.prmtop \
  #~ -ref ExWaterPep_minsolv.rst7 \
  #~ -r   ExWaterPep_minpro.rst7
#~ 
#~ /cottus/opt/amber11-dev/bin/mpirun -np 4 $EXE -O \
  #~ -i   Exminall.in \
  #~ -o   Exminall.out \
  #~ -c   ExWaterPep_minpro.rst7 \
  #~ -p   ExWaterPep.prmtop \
  #~ -ref ExWaterPep_minpro.rst7 \
  #~ -r   ExWaterPep_minall.rst7


