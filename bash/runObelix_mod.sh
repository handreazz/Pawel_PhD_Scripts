#!/bin/csh
#
#PBS -N Eq1
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o Eq2.out
#PBS -e Eq2.err
#PBS -V

# Change to my working directory
set NETDIR="/home/pjanowsk/Case/pepsim/Run2"
cd ${NETDIR}

# Create subdirectories for results if they do not already exist
mkdir -p Restart/ Energy/ Trajectory/ OutDiags/

# Copy the final equilibration restart and make that the initial
# production run restart
cp ../prep/equil/solvpep_Eq9.rst Restart/md0.rst

# Create a directory on the node scratch disk for our work
set NODEDIR="/scratch/pjanowsk/pepsim/"
mkdir -p ${NODEDIR}
cd ${NODEDIR}

# Start lam MPI
#/cottus/opt/amber11/bin/lamboot

set H = 1
set I = 1
set IM = 0
set RSEED = 210381
while ( ${I} <= 500 )

  # Test for existence of the restart file
  if ( ! -e ${NETDIR}/Restart/md${I}.rst ) then

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
    if ( ! -e ${NETDIR}/Restart/md${I}.rst) then
      cp ${NETDIR}/solvpep.top .
      cp ${NETDIR}/Restart/md${IM}.rst .
#      mpirun -np 8 /cottus/opt/amber11/bin/pmemd -O \
#      pmemd -O \
      set LD_LIBRARY_PATH = (${AMBERHOME}/src/netcdf/lib ${LD_LIBRARY_PATH})
      mpirun -np 8 /home/pjanowsk/amber11/bin/pmemd -O \
          -i md.in \
          -o md${I}.out \
          -p solvpep.top \
          -c md${IM}.rst \
          -r md${I}.rst \
          -x md${I}.crd \
          -e md${I}.en \
          < /dev/null

      # Move files back to network directories
      mv md${I}.out ${NETDIR}/OutDiags/
      mv md${I}.en  ${NETDIR}/Energy/
      mv md${I}.crd ${NETDIR}/Trajectory/
      mv md${I}.rst ${NETDIR}/Restart/

      # Increment counter H to tell us that we have
      # completed one more segment during this job
      # submission cycle
      @ H+=1
    endif

    # Once we have completed 8 segments on this job
    # submission cycle, exit completely
    if (${H} > 2) then
      break
    endif

  endif

  # Increment the counter variable
  @ I+=1
  @ IM+=1
  @ RSEED+=1

end

#/cottus/opt/amber11/bin/lamhalt

rm -r ${NODEDIR}

