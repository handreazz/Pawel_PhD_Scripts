#!/bin/bash
#PBS -l nodes=10:ppn=16:native
#PBS -l walltime=22:00:00
#PBS -q normal
#PBS -m abe
#PBS -M radakb@biomaps.rutgers.edu
#PBS -V

cd $PBS_O_WORKDIR
EXE=`which pmemd.MPI` # After putting "module load amber/12" in my bashrc

PROJECT=HDV/U-1
MLC=blt_rt_C41p
MGstate=Mg

SDIR=$SCRATCH/$PROJECTS/${MLC}_M2_FEP/equilibration
cd $SDIR

PRM=../initial/${MLC}_${MGstate}_FEP_initial.prmtop
LABEL=heating
INP=$LABEL.inp
OUT=${MGstate}_$LABEL.out
CRD=${MGstate}_minimize.rst7
RST=${MGstate}_$LABEL.rst7
XYZ=${MGstate}_$LABEL.nc
INF=${MGstate}_$LABEL.info
REF=$CRD

ARGS="-O -i $INP -p $PRM -c $CRD -o $OUT -r $RST -x $XYZ -inf $INF -ref $REF -suffix $MGstate"
mpirun_rsh -np 160 -hostfile $PBS_NODEFILE $EXE $ARGS & # <-- Note mpirun_rsh and -hostfile
wait

