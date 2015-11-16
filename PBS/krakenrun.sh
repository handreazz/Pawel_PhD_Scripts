#!/bin/bash
#

set -x
NP=120

#EQFILE=equil30.rst7
TOPO=topo.prmtop
SimsToRun=1

#Rename minimized structure
#mkdir -p Out Restart Trajectory Energy
#cp ${EQFILE} Restart/md0.rst7


#Loop
I=1
let IM=$I-1
RunCount=0


#Create input file
cat > md.in << EOF
Standard MD run input
 &cntrl

  nmropt = 0,
  ntx    = 5,       irest  = 1,
  ntrx   = 1,       ntxo   = 1,
  ntpr   = 10000,   ntwx   = 10000,
  ntwv   = 0,       ntwe   = 10000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = 2,
  es_cutoff   = 10.0,
  vdw_cutoff  = 10.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 2200000,
  nscm   = 10000,
  t      = 0.0,     dt     = 0.001,

  temp0     = 300.0,   tempi  = 300.0,
  ig        = -1,
  ntt       = 3,
  gamma_ln = 1.0,

  ntp    = 1,       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
EOF


#run simulation

while [ ${RunCount} -lt ${SimsToRun} ]; do  #as long as the number of sims to run hasn't been reached
  if [ ! -e md${I}.rst7 ]; then      #see if the Restart exits, if not run sim
    aprun -n $NP /nics/a/proj/CHE100072/amber040411/bin/pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p ${TOPO} \
          -c md${IM}.rst7 \
          -r md${I}.rst7 \
          -x md${I}.nc \
          -e md${I}.en
    let RunCount=RunCount+1   #incerment only if sim was run
  fi

  let I=I+1     #increment always
  let IM=IM+1
done

  
  #~ if [ ${SimsRun} ge 1 ]; then
      #~ break
  #~ fi


