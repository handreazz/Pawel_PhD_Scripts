#!/bin/bash
#

set -x

TOPO=topo.prmtop
NP=120
MINFILE=Eq0.rst7
EQFILE=Eq9.rst7

PNUM=0
NUM=1

for RESTWT in 256.0 64.0 16.0 4.0 1.0 0.5 0.25 0.125 0.0625
do
  NSTEP=50000
  TSTEP=0.0015
  NTX=5
  IREST=1
  NTB=1
  NPT=0
  if [ ${NUM} -eq 1 ]; then
    NSTEP=50000
    TSTEP=0.001
    NTX=1
    IREST=0
  fi
  if [ ${NUM} -gt 4 ]; then
    TSTEP=0.002
    NTB=2
    NPT=1
  fi


cat > Eq${PNUM}.in << EOF
Standard MD run file
 &cntrl

  nmropt = 0,
  ntx    = ${NTX},       irest  = ${IREST},       ntrx   = 1,      ntxo   = 1,
  ntpr   = 1000,    ntwx   = 1000,    ntwv   = 0,      ntwe   = 1000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = ${NTB},
  es_cutoff     = 10.0,
  vdw_cutoff    = 10.0,

  ibelly = 0,       ntr    = 1,

  imin   = 0,
  nstlim = ${NSTEP},
  nscm   = 1000,
  t      = 0.0,     dt     = ${TSTEP},

  temp0     = 300.0,   tempi  =  0.0,
  ig        = -1,
  ntt       = 3,
  gamma_ln  = 3.0,
  vlimit    = 20.0,

  ntp    = ${NPT},       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
Hold protein fixed
${RESTWT}
FIND
* * M *
* * S *
* * B *
* * 3 *
* O2 * *
* O * *
SEARCH
RES 1 720
END
END
EOF


  if [ ! -e Eq${NUM}.rst7 ]; then
    aprun -n $NP /nics/a/proj/CHE100072/amber040411/bin/pmemd.MPI -O \
      -i Eq${PNUM}.in \
      -o Eq${NUM}.out \
      -c Eq${PNUM}.rst7 \
      -r Eq${NUM}.rst7 \
      -ref Eq${PNUM}.rst7 \
      -p $TOPO \
      -e Eq${NUM}.en 
  fi

  let NUM=NUM+1
  let PNUM=PNUM+1

done

####1ns MD run
cp ${EQFILE} md0.rst7

#Loop
I=1
IM=0

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
  nstlim = 1500000,
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

aprun -n $NP /nics/a/proj/CHE100072/amber040411/bin/pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p $TOPO \
          -c md${IM}.rst7 \
          -r md${I}.rst7 \
          -x md${I}.nc \
          -e md${I}.en

