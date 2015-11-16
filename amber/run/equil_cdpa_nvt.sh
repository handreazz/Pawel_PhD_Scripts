#!/bin/bash
#
#PBS -N Cdp_UCA_eq
#PBS -l nodes=1
#PBS -l walltime=24:00:00
#PBS -o Cdp_UCAeq.out
#PBS -e Cdp_UCAeq.err
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

for RESTWT in 256.0 100.0 10.0 1.0 0.1
 do
   NTX=5
   IREST=1
   NMROPT=0
   if [ ${NUM} -eq 1 ]; then
     NSTEP=300000
     NTX=1
     IREST=0
     NMROPT=1
     RESTZINC=256.0
   fi
   if [ ${NUM} -eq 2 ]; then
     NSTEP=2000000
     RESTZINC=256.0
   fi
   if [ ${NUM} -eq 3 ]; then
     NSTEP=2000000
     RESTZINC=100.0
   fi
   if [ ${NUM} -gt 4 ]; then
     NSTEP=2000000
     RESTZINC=100.0
   fi
   if [ ${NUM} -eq 5 ]; then
     NSTEP=2000000
     RESTZINC=100.0
   fi

cat > mdequil${PNUM}.in << EOF
Standard MD run file
 &cntrl
  nmropt = ${NMROPT},
  ntx    = ${NTX},
  irest  = ${IREST},
  nstlim = ${NSTEP},
  
  ntb    = 1,           !Constant volume
  ntp    = 0,           !Turn off barostat

  es_cutoff     =  8.0,
  vdw_cutoff    = 10.0,  
  iwrap  = 0,           !Wrapping off
    
  ntrx   = 1,           !Output settings
  imin   = 0,           !Not minimization
  ntpr   = 1000,        !Print energy to output    
  ntwx   = 1000,        !Print trajectory
  ntwr   = 1000,        !Print restart
  ntwv   = 0,           !Don't print velocy file
  ntwe   = 0,           !Don't print energy file
  ioutfm = 1,           !Trajectory in netcdf
  t      = 0.0,         !Start time
  dt     = 0.001,       !Time step
  
  ntf    = 2,           !SHAKE all H atoms 
  ntc    = 2,           !Use SHAKE
  tol    = 0.000001, 	!SHAKE tolerance
  watnam = 'WAT ',      !Water residue name
   
  ibelly = 0,           !Constraints off
  ntr    = 1,           !Restraints on

  ntt       = 3,        !Langevin thermostat
  temp0     = 295.0     !Target temperature
  ig        = -1,       !Random seed
  gamma_ln  = 1.0,      !Langevin collision freq
  vlimit    = 20.0,     !Safe velocity limit
  nscm   = 1000,        !Reset center of mass translation
  
  pres0  = 1.0,
  comp   = 44.6,
  taup   = 1.0,
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
      -p $TOPO
    cp Eq${NUM}.rst7 ${NETDIR}
    mv Eq${NUM}.out ${NETDIR}
  fi

  let NUM=NUM+1
  let PNUM=PNUM+1

done



#clean scratch
#rm -r ${NODEDIR}
