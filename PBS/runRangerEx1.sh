#! /bin/bash
#
#$ -V
#$ -N ExRuntest1
#$ -e ExEqtest1.err
#$ -M pawelrc@gmail.com
#$ -m be
#$ -l h_rt=24:00:00
#$ -o ExEqtest1.out
#$ -pe 16way 32            # Requests 16 cores/node, 16/32 = 2 nodes total
#$ -q normal
#

NETDIR=/share/home/01682/pawelrc/testamber/prod
TOPO=/share/home/01682/pawelrc/testamber/ExWaterPep.top
COORD=/share/home/01682/pawelrc/testamber/test1/ExWaterPep_Eq9.rst

# Change to my working directory
cd ${NETDIR}
# Create subdirectories for results if they do not already exist
mkdir -p RunEx/Restart/ RunEx/Energy/ RunEx/Trajectory/ RunEx/OutDiags/

# Copy the final equilibration restart and make that the initial
# production run restart
cp ${COORD} RunEx/Restart/md0.rst


# Create a directory on the node scratch disk for our work
#set NODEDIR="/scratch/pawelrc/ExRun/"
#mkdir -p ${NODEDIR}
#cd ${NODEDIR}



set H = 1
set I = 1
set IM = 0
set RSEED = 210481
while ( ${I} <= 2500 )

  # Test for existence of the restart file
  if ( ! -e ${NETDIR}/RunEx/Restart/md${I}.rst ) then

cat > md.in << EOF
Standard MD run input
 &cntrl

  nmropt = 0,
  ntx    = 5,       irest  = 1,
  ntrx   = 1,       ntxo   = 1,
  ntpr   = 10000,   ntwx   = 10000,
  ntwv   = -1,       ntwe   = 10000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = 2,
  es_cutoff   =  8.0,
  vdw_cutoff  = 12.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 100000,
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


    # Run the MD simulation
    if ( ! -e ${NETDIR}/RunEx/Restart/md${I}.rst) then
#      cp ${NETDIR}/ExWaterPep.top .
#      cp ${NETDIR}/RunEx/Restart/md${IM}.rst .

      ibrun pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p ${TOPO} \
          -c ${NETDIR}/RunEx/Restart/md${IM}.rst \
          -r md${I}.rst \
          -x md${I}.crd \
          -e md${I}.en \
          < /dev/null

      # Move files back to network directories
      mv md${I}.out ${NETDIR}/RunEx/OutDiags/
      mv md${I}.en  ${NETDIR}/RunEx/Energy/
      mv md${I}.crd ${NETDIR}/RunEx/Trajectory/
      mv md${I}.rst ${NETDIR}/RunEx/Restart/

      # Increment counter H to tell us that we have
      # completed one more segment during this job
      # submission cycle
      @ H+=1
    endif

    # Once we have completed 8 segments on this job
    # submission cycle, exit completely
    if (${H} > 3) then
      break
    endif

  endif

  # Increment the counter variable
  @ I+=1
  @ IM+=1
  @ RSEED+=1

end

#lamhalt

#rm -r ${NODEDIR}
