#!/bin/bash

set -x

#define variables
MPIR=/nics/a/proj/CHE100072/NAMD_2.7_Source/CRAY-XT-Linux-GNU4.41/charmrun
EXE=/nics/a/proj/CHE100072/NAMD_2.7_Source/CRAY-XT-Linux-GNU4.41/namd2
NP=240
SimsToRun=2

#Loop
I=1
let IM=$I-1
RunCount=0

while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
  if [ ! -e md${I}.coor ]; then      #see if the Restart exits, if not run sim

#### if this is the first run, set to flag the bincoordinates, binvelocities and extendedSystem commands below and unflag the temperature
bincoord=
tempfl=#
if [ ${I} == 1 ]; then
	bincoord=#
        tempfl=
fi

# CREATE INPUT
cat > namd.in << EOF
#############################################################
##                                                         ##
##   ADD THE DESCRIPTION HERE !!!!!                        ##
##                                                         ##
#############################################################

source OUT.settings
source NPT.settings
source PME.settings
waterModel tip4

${bincoord}bincoordinates md${IM}.coor
${bincoord}binvelocities  md${IM}.vel
${bincoord}extendedSystem md${IM}.xsc
${tempfl}temperature 300
outputName     md${I}

parmfile topo.prmtop
ambercoor equil30.rst7
timestep       1.0    	;# 1fs/step (dt=0.001 in amber)
${tempfl}minimize 2000
run 3000000
EOF

   #RUN SIMULATION
   aprun -n ${NP} $EXE namd.in > ${I}.log
   let RunCount=RunCount+1   		#incerment only if sim was run
  fi

  let I=I+1     			#increment always
  let IM=IM+1
done

#clean scratch
#rm -r ${NODEDIR}

