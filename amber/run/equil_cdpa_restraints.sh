#!/bin/bash
#
#PBS -N 1rpgKeq
#PBS -l nodes=1
#PBS -l walltime=24:00:00
#PBS -o 1rpgKeq.out
#PBS -e 1rpgKeq.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/ifortvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/bin/intel64/iccvars_intel64.sh
source /cottus/opt/intel/Compiler/11.1/072/mkl/tools/environment/mklvarsem64t.sh
INTEL_LICENSE_FILE=/cottus/opt/intel/Compiler/11.1/069/licenses 
source /cottus/opt/intel_2013/composer_xe_2013.1.117/bin/iccvars.sh intel64
source /cottus/opt/intel_2013/composer_xe_2013.1.117/bin/compilervars.sh intel64
set -x

#define variables
NAME=Cdp_UCA
NETDIR=$PBS_O_WORKDIR
NODEDIR="/scratch/pjanowsk/${NAME}/"
MINFILE=${NAME}_minall.rst7
TOPO=${NAME}.prmtop
NP=48
EXE=/cottus/home/pjanowsk/amberSD/bin/pmemd.MPI
MPIR=/cottus/opt/amber11-dev/bin/mpirun

#Rename minimized structure
cd ${NETDIR}
cp ${MINFILE} Eq0.rst7

#Change to scratch directory and copy files from NETDIR
mkdir -p ${NODEDIR}
cd ${NODEDIR}
cp ${NETDIR}/Eq0.rst7 .
cp ${NETDIR}/$TOPO .

# Restrained Equilibration all at constant volume
PNUM=0
NUM=1

for RESTWT in 256.0 100.0 16.0 4.0 1.0 0.5 0.25 0.125 0.0625
do
  NSTEP=1000000
  TSTEP=0.0015
  NTX=5
  IREST=1
  NTB=1
  NPT=0
  NMROPT=0
  RESTZINC=100.0
  if [ ${NUM} -eq 1 ]; then
    NSTEP=300000
    TSTEP=0.001
    NTX=1
    IREST=0
    NMROPT=1
    RESTZINC=256.0 
  fi
  if [ ${NUM} -gt 4 ]; then
    TSTEP=0.001
    NTB=2
    NPT=1
  fi


cat > mdequil${PNUM}.in << EOF
Standard MD run file
 &cntrl

  nmropt = ${NMROPT},
  ntx    = ${NTX},       irest  = ${IREST},       ntrx   = 1,      ntxo   = 1,
  ntpr   = 1000,    ntwx   = 1000,    ntwv   = 0,      ntwe   = 1000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = ${NTB},
  es_cutoff     =  8.0,
  vdw_cutoff    = 10.0,

  ibelly = 0,       ntr    = 1,

  imin   = 0,
  nstlim = ${NSTEP},
  nscm   = 1000,
  t      = 0.0,     dt     = ${TSTEP},

  temp0     = 295.0,   tempi  =  0.0,
  ig        = -1,
  ntt       = 3,
  gamma_ln  = 3.0,
  vlimit    = 20.0,

  ntp    = ${NPT},       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
 /
 &wt
   type='TEMP0', istep1=0,     istep2=295000,
	         value1=0.0,  value2=295.0,
 /
 &wt
   type='END',
 /
Restraint for solute
${RESTWT}
RES 1 120 
END
Restraint for zinc1
${RESTZINC}
RES 18 18
END
Restraint for zinc2
${RESTZINC}
RES 47 47
END
Restraint for zinc3
${RESTZINC}
RES 58 60 
END
Restraint for zinc4
${RESTZINC}
RES 78 78
END
Restraint for zinc5
${RESTZINC}
RES 107 107
END
Restraint for zinc6
${RESTZINC}
RES 118 120 
END
END
EOF


  if [ ! -e Eq${NUM}.rst7 ]; then
    $MPIR -np $NP $EXE -O \
      -i mdequil${PNUM}.in \
      -o Eq${NUM}.out \
      -c Eq${PNUM}.rst7 \
      -r Eq${NUM}.rst7 \
      -ref Eq${PNUM}.rst7 \
      -p $TOPO \
      -e Eq${NUM}.en 
    cp Eq${NUM}.rst7 ${NETDIR}
    mv Eq${NUM}.out Eq${NUM}.en ${NETDIR}
  fi

  let NUM=NUM+1
  let PNUM=PNUM+1

done

#clean scratch
rm -r ${NODEDIR}
