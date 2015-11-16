#!/bin/csh
#
#PBS -N Eq1
#PBS -l nodes=1:ppn=8
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o Eq1.out
#PBS -e Eq1.err
#PBS -V

# Change to my working directory
set NETDIR="/home/pjanowsk/Case/pepsim"
cd ${NETDIR}

# Create subdirectories for results if they do not already exist
#mkdir -p Run/Restart/ Run/Energy/ Run/Trajectory/ Run/OutDiags/

# Copy the final equilibration restart and make that the initial
# production run restart
#cp /home/pjanowsk/Case/pepsimprep/equil/solvpep_Eq9.rst Run/Restart/md0.rst

# Create a directory on the node scratch disk for our work
set NODEDIR="/scratch/pjanowsk/pepsim/"
mkdir -p ${NODEDIR}
cd ${NODEDIR}

#lamboot

set H = 1
set I = 1
set IM = 0
set RSEED = 210481
while ( ${I} <= 2000 )

  # Test for existence of the restart file
  if ( ! -e ${NETDIR}/Run/Restart/md${I}.rst ) then

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
    if ( ! -e ${NETDIR}/Run/Restart/md${I}.rst) then
      cp ${NETDIR}/prep/solvpep.top .
      cp ${NETDIR}/Run/Restart/md${IM}.rst .
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
      mv md${I}.out ${NETDIR}/Run/OutDiags/
      mv md${I}.en  ${NETDIR}/Run/Energy/
      mv md${I}.crd ${NETDIR}/Run/Trajectory/
      mv md${I}.rst ${NETDIR}/Run/Restart/

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
  @ RSEED+=1

end

#lamhalt

#rm -r ${NODEDIR}

