
#!/bin/bash
#
#PBS -A TG-CHE100072
#PBS -N 7xRun
#PBS -o 2.out
#PBS -e 2.err
#PBS -l walltime=24:00:00,size=840
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x
cd $PBS_O_WORKDIR

for j in 2oueIb 2oueSg 2p7eSi 3cqsSi p2oueSb p2p7eSb p3cqsSd
do
	cd $PBS_O_WORKDIR
	cd ${j}
	./krakenrun.sh &
done

wait

