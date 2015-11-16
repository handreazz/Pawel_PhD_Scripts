#!/bin/bash
set -x

TOPO=topo.prmtop
STEPS=7
NP=160
EXE=`which pmemd.MPI`

#Loop
for (( I = 1; I <= ${STEPS}; I++ ))
do
    let J=I-1
    if [ ! -e Restart/equil${I}.rst7 ]; then
    mpirun_rsh -hostfile nodes.dat -n $NP $EXE -O \
      -i equil${I}.in \
      -o Out/equil${I}.out \
      -c Restart/equil${J}.rst7 \
      -r Restart/equil${I}.rst7 \
      -ref Restart/equil${J}.rst7 \
      -p $TOPO \
      -e equil${I}.en
    fi
done




