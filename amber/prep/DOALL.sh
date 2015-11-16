#!/bin/bash -f 

set -x


## is prepscript_new prepared with correct solvent to add and initial file?
## input variable should be just the letter

NAME=$1
ROOT=/home/pjanowsk/York/1rpg
TOPO=amb_${NAME}.prmtop
RST=${NAME}.rst7


cd ${ROOT}
cd prep
./prepscript${NAME}.sh ${NAME}

cd ../equil_amber
mkdir ${NAME}
cd ${NAME}
cp ../../minimization/G/minimize_krakow.sh .
cp ../../prep/$TOPO .
cp ../../prep/$RST .
cp ../G/equilibrate_tyr.sh .
cp ../G/run_tyr.sh .


