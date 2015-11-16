#!/bin/csh
#
#PBS -N pepsimNVE
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o pepsimNVE.out
#PBS -e pepsimNVE.err
#PBS -V

# Change to my working directory
set NETDIR="/home/pjanowsk/Case/pepsim"
cd ${NETDIR}

# Create subdirectories for results if they do not already exist
mkdir -p NVE/Restart/ NVE/Energy/ NVE/Trajectory/ NVE/OutDiags/

# Copy the final equilibration restart and make that the initial
# production run restart
cp /home/pjanowsk/Case/pepsim/prep/equil/solvpep_Eq9.rst NVE/Restart/md0.rst

# Create a directory on the node scratch disk for our work
set NODEDIR="/scratch/pjanowsk/pepsim/"
mkdir -p ${NODEDIR}
cd ${NODEDIR}

#lamboot

set H = 1
set I = 1
set IM = 0
while ( ${I} <= 2000 )

  # Test for existence of the restart file
  if ( ! -e ${NETDIR}/NVE/Restart/md${I}.rst ) then

cat > md.in << EOF
Standard MD run input
 &cntrl

  nmropt = 0,
  ntx    = 5,       irest  = 1,
  ntrx   = 1,       ntxo   = 1,
  ntpr   = 10000,   ntwx   = 10000,
  ntwv   = -1,       ntwe   = 10000,
  iwrap  = 0,       ioutfm = 1,

  ntf    = 2,       ntb    = 1,
  es_cutoff   =  8.0,
  vdw_cutoff  = 12.0,

  ibelly = 0,       ntr    = 0,

  imin   = 0,
  nstlim = 100000,
  nscm   = 10000,
  t      = 0.0,     dt     = 0.002,

  temp0     = 277.0,
  ntt       = 0,

  ntp    = 0,       pres0  = 1.0,     comp   = 44.6,
  taup   = 1.0,

  ntc    = 2,       tol    = 0.000001, watnam = 'WAT ',

 &end
EOF

    # Run the MD simulation
    if ( ! -e ${NETDIR}/NVE/Restart/md${I}.rst) then
      cp ${NETDIR}/prep/solvpep.top .
      cp ${NETDIR}/NVE/Restart/md${IM}.rst .
#      export PATH="$AMBERHOME/bin:$PATH"
#      export LD_LIBRARY_PATH="$AMBERHOME/src/netcdf/lib:$LD_LIBRARY_PATH"
#      set LD_LIBRARY_PATH = (${AMBERHOME}/src/netcdf/lib ${LD_LIBRARY_PATH})
#      mpirun -np 8 /cottus/opt/amber11/bin/pmemd -O \

      mpirun -np 8 pmemd.MPI -O \
          -i md.in \
          -o md${I}.out \
          -p solvpep.top \
          -c md${IM}.rst \
          -r md${I}.rst \
          -x md${I}.crd \
          -e md${I}.en \
          < /dev/null

      # Move files back to network directories
      mv md${I}.out ${NETDIR}/NVE/OutDiags/
      mv md${I}.en  ${NETDIR}/NVE/Energy/
      mv md${I}.crd ${NETDIR}/NVE/Trajectory/
      mv md${I}.rst ${NETDIR}/NVE/Restart/

      # Increment counter H to tell us that we have
      # completed one more segment during this job
      # submission cycle
      @ H+=1
    endif

    # Once we have completed 8 segments on this job
    # submission cycle, exit completely
    if (${H} > 50) then
      break
    endif

  endif

  # Increment the counter variable
  @ I+=1
  @ IM+=1

end

#lamhalt

rm -r ${NODEDIR}

