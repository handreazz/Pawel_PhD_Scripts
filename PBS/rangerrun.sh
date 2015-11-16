#! /bin/bash
#
#$ -V
#$ -N hpIcrun
#$ -e hpIcrun.err
#$ -o hpIcrun.out
#$ -M pawelrc@gmail.com
#$ -m bea
#$ -l h_rt=24:00:00
#$ -pe 16way 128            # Requests 16 cores/node, 16/32 = 2 nodes total
#$ -q normal
#$ -cwd
#


set -x
JOBID=$JOB_ID
NAME=$JOB_NAME
WORKDIR=$NAME.$JOBID

# Provide NETDIR
NETDIR=${HOME}/runIc
EQFILE=hpinIc_Eq9.rst7
TOPO=XtalxIc.prmtop
RSEED=8174

#Rename minimized structure
cd ${NETDIR}
cp ${NETDIR}/${EQFILE} md0.rst7
#Change to scratch directory and copy files from NETDIR
NODEDIR=${WORK}/${WORKDIR}
mkdir -p ${NODEDIR}
cd ${NODEDIR}
cp ${NETDIR}/md0.rst7 .
cp ${NETDIR}/$TOPO .

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
  es_cutoff   =  8.0,
  vdw_cutoff  = 12.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 500000,
  nscm   = 10000,
  t      = 0.0,     dt     = 0.002,

  temp0     = 277.0,   tempi  = 277.0,
  ig        = ${RSEED},
  ntt       = 2,

  ntp    = 1,       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
EOF

let RSEED=RSEED+1


#Run Simulation

  #if [ ! -e md1.rst ]; then
      ibrun pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p ${TOPO} \
          -c md${IM}.rst7 \
          -r md${I}.rst7 \
          -x md${I}.nc \
          -e md${I}.en \
          < /dev/null
      #cp ${BFIX}_Eq${NUM}.out ${BFIX}_Eq${NUM}.rst ${BFIX}_Eq${NUM}.en ${NETDIR}
  #fi

  let I=I+1
  let IM=IM+1


mv *.out ${NETDIR}
mv *.rst7 ${NETDIR}
mv *.en ${NETDIR}
mv *.nc ${NETDIR}

#rm -r ${NODEDIR}
