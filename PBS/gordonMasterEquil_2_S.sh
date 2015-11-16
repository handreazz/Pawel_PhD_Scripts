#!/bin/bash
#PBS -A TG-MCB110101
#PBS -N CdpEquilS
#PBS -o Sequil2.out
#PBS -e Sequil2.err
#PBS -l nodes=10:ppn=16:native
#PBS -l walltime=19:00:00
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x
cd $PBS_O_WORKDIR
#cd /oasis/scratch/pawelrc/temp_project
STEP=2
NP=160

cp $PBS_NODEFILE allnodes.dat
counter=0

for j in S/
do
	cd $PBS_O_WORKDIR
	sed -n $[$counter*$NP+1],$[$counter*$NP+$NP]p allnodes.dat >nodes.dat
	cp nodes.dat ${j}
	cd ${j}
	./equilibrate_gordon_${STEP}.sh &
	let counter=counter+1
done

wait

