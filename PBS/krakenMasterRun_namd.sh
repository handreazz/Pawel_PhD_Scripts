#!/bin/bash
#
#PBS -A TG-CHE100072
#PBS -N run6x
#PBS -l walltime=24:00:00,size=1440
#PBS -M pawelrc@gmail.com
#PBS -m bea


######################################
####     CHECKLIST          ##########
#
# OUT.settings
# NPT.settings
# PME.settings
# md1.coor   ###these three files only if restart from namd, if from amber, don't need.
# md1.vel    ###if restart from namd modify the lines in namd.in below (uncomment lines)
# md1.xsc 
# topo.prmtop
# equil30.rst7
#
######################################


set -x
cd $PBS_O_WORKDIR

for j in 2oueIb_ff10 3cqsIe_ProdEquil p2p7eIa_ProdEquil 2p7eIh_ProdEquil krakenMasterRun.sh p2oueIa_ProdEquil p3cqsIa_ProdEquil

do
	cd $PBS_O_WORKDIR
	cd ${j}
	cp ../kraken_namd.sh .
	./kraken_namd.sh &
done

wait

