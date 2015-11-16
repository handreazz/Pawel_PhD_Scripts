#!/bin/bash
#PBS -A TG-MCB110101
#PBS -N Equil1
#PBS -o 1.out
#PBS -e 1.err
#PBS -l nodes=10:ppn=16:native
#PBS -l walltime=24:00:00
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x
cd $PBS_O_WORKDIR
#cd /oasis/scratch/pawelrc/temp_project
STEP=1

for j in p2p7e_equil2/
do
	cd $PBS_O_WORKDIR
	cp gordonequil${STEP}.sh ${j}	
	cd ${j}
	./gordonequil${STEP}.sh &
done

wait

