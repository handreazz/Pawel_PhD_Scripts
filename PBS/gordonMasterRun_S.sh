#!/bin/bash
#PBS -A TG-MCB110101
#PBS -N CdpRunS
#PBS -o CdpSRun.out
#PBS -e CdpSRun.err
#PBS -l nodes=10:ppn=16:native
#PBS -l walltime=19:00:00
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x
cd $PBS_O_WORKDIR
#cd /oasis/scratch/pawelrc/temp_project
STEP=1
NP=160

cp $PBS_NODEFILE allnodes.dat
counter=0

for j in S/ 
do
	cd $PBS_O_WORKDIR
	sed -n $[$counter*$NP+1],$[$counter*$NP+$NP]p allnodes.dat >nodes.dat
	cp nodes.dat ${j}
	cd ${j}
	./run_gordon.sh &
	let counter=counter+1
done

wait

