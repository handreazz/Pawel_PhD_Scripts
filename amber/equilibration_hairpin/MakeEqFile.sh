#!/bin/bash

#1. minimize 2000 steps (conjugate gradient, if you think it matters)
#2. NVT, heat up to 100 K at a rate of 1 K per ps
#3. NPT, heat up to 300 K at 1 K per ps
#4. NPT, 500 ps at 300 K

#First round of simulated annealing
#5. NVT, heat up to 600 K at 1 K per ps
#6. NVT, 500 ps at 600 K
#7. NVT, cool down to 300 K at 1 K per ps
#8. NVT, 1.5 ns at 300 K
#9. NPT, 3 ns at 300 K

#Second round of simulated annealing:
#10. NVT, heat up to 600 K at 1 K per ps
#11. NVT, 500 ps at 600 K
#12. NVT, cool down to 300 K at 1 K per ps
#13. NVT, 1.5 ns at 300 K
#14. NPT, 3 ns at 300 K

#Scale down the constraints (exponential decay, with half-life parameter of 100 ps)
#15. minimize 2000 steps
#16. NPT, heat up to 300 K at 1 K per ps.
#17. NPT, 500 ps at 300 K
#18. NPT, 50 ps at 300 K, scale constraints by 0.7071
#19. NPT, 50 ps at 300 K, scale constraints by 0.5000
#20. NPT, 50 ps at 300 K, scale constraints by 0.3536
#21. NPT, 50 ps at 300 K, scale constraints by 0.2500
#22. NPT, 50 ps at 300 K, scale constraints by 0.1768
#23. NPT, 50 ps at 300 K, scale constraints by 0.1250
#24. NPT, 50 ps at 300 K, scale constraints by 0.0884
#25. NPT, 50 ps at 300 K, scale constraints by 0.0625
#26. NPT, 50 ps at 300 K, scale constraints by 0.0442
#27. NPT, 50 ps at 300 K, scale constraints by 0.0312

#Final MD
#28. minimize 2000
#29. NPT, heat to 300K at 1 K per ps.
#30. NPT, 10 ns at 300 K 

set -x

for (( STEP = 1; STEP <= 30; STEP++ ))
do
NTR=1

	if [ ${STEP} -eq 1 ]; then
		./MakeRestraints.py 1.0
		HEAT=minimize
	fi
	if [ ${STEP} -eq 2 ]; then
		INIT=yes        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=100.0       ##target temperature
		NSTLIM=100000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 3 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=200000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=100.0
	fi
	if [ ${STEP} -eq 4 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 5 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=600.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=300.0
	fi
	if [ ${STEP} -eq 6 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=600.0       ##target temperature
		NSTLIM=500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 7 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=600.0
	fi
	if [ ${STEP} -eq 8 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=1500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 9 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=2000000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 10 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=600.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=300.0
	fi
	if [ ${STEP} -eq 11 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=600.0       ##target temperature
		NSTLIM=500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 12 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=600.0
	fi
	if [ ${STEP} -eq 13 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NVT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=1500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 14 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=2000000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 15 ]; then
		HEAT=minimize
	fi
	if [ ${STEP} -eq 16 ]; then
		INIT=yes        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 17 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=500000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
	fi
	if [ ${STEP} -eq 18 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.7071
	fi
	if [ ${STEP} -eq 19 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.5000
	fi
	if [ ${STEP} -eq 20 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.3536
	fi
	if [ ${STEP} -eq 21 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.2500
	fi
	if [ ${STEP} -eq 22 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.1768
	fi
	if [ ${STEP} -eq 23 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.1250
	fi
	if [ ${STEP} -eq 24 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.0884
	fi
	if [ ${STEP} -eq 25 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.0625
	fi
	if [ ${STEP} -eq 26 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.0442
	fi
	if [ ${STEP} -eq 27 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=50000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		./MakeRestraints.py 0.0312
	fi
	if [ ${STEP} -eq 28 ]; then
		HEAT=minimize
		NTR=0
	fi
	if [ ${STEP} -eq 29 ]; then
		INIT=yes        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=300000    ###length of simulation 50000=50ps
		HEAT=yes        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		NTR=0
        fi
	if [ ${STEP} -eq 30 ]; then
		INIT=no        ##no or yes (yes if first step after minimization)
		ENSEMBLE=NPT    ##NVT or NPT
		TEMP=300.0       ##target temperature
		NSTLIM=2000000    ###length of simulation 50000=50ps
		HEAT=no        ##yes or no (yes if heating or cooling)(check)
		ITEMP=0.0
		NTR=0
        fi

	#####
	if [ ${INIT} = "yes" ]; then
	  IREST=0
	  NTX=1
	else
	  IREST=1
	  NTX=5
	fi

	if [ ${ENSEMBLE} = "NVT" ]; then
	  NTP=0
	  NTB=1
	elif [ ${ENSEMBLE} = "NPT" ]; then
	  NTP=1
	  NTB=2
	fi

	####

	if [ ${HEAT} = "no" ]; then
cat > tmp.in << EOF
Minimize Hairpin solvent and ions
 &cntrl
  imin   = 0,           !No minimization
  irest  = ${IREST},    !This is not a restart 	     
  iwrap  = 0,           !Don't rap the coordinates
  ntx    = ${NTX},      !No initial velocity is read 
  ntp    = ${NTP},      !No constant pressure        
  ntb    = ${NTB},      !Constant Volume PB          
  cut    = 10,          !Non-bonded cutoff
  ntr    = ${NTR}       !Use restraints
  ntc    = 2,           !Use SHAKE to constrain H's
  ntf    = 2,           !Shake all H atoms
  temp0  = ${TEMP},     !Target temp	            
  ntt    = 3,           !Use Langevin temp scaling
  gamma_ln = 1.0,       !Langevin collision freq
  nstlim = ${NSTLIM},   !Number of timesteps        
  dt = 0.001,           !Timestep in ps
  ntpr = 1000,          !Print to output
  ntwx = 1000,          !Print to mdcrd
  ioutfm = 1,           !Binary trajectory
  ntwr = 1000           !Print to restart file
  ig     = -1
 &end
EOF
	fi



	if [ ${HEAT} = "yes" ]; then
cat > tmp.in << EOF
Minimize Hairpin solvent and ions
 &cntrl
  nmropt = 1
  imin   = 0,           !No minimization
  irest  = ${IREST},    !This is not a restart 	     
  iwrap  = 0,           !Don't rap the coordinates
  ntx    = ${NTX},      !No initial velocity is read 
  ntp    = ${NTP},      !No constant pressure        
  ntb    = ${NTB},      !Constant Volume PB          
  cut    = 10,          !Non-bonded cutoff
  ntr    = ${NTR},      !Use restraints
  ntc    = 2,           !Use SHAKE to constrain H's
  ntf    = 2,           !Shake all H atoms
  temp0  = ${TEMP},     !Target temp	            
  ntt    = 3,           !Use Langevin temp scaling
  gamma_ln = 1.0,       !Langevin collision freq
  nstlim = ${NSTLIM},   !Number of timesteps        
  dt = 0.001,           !Timestep in ps
  ntpr = 1000,          !Print to output
  ntwx = 1000,          !Print to mdcrd
  ioutfm = 1,           !Binary trajectory
  ntwr = 1000           !Print to restart file
  ig     = -1
 &end
 &wt
   type='TEMP0', istep1=0,     istep2=${NSTLIM},
	         value1=${ITEMP},  value2=${TEMP},
 &end
 &wt
   type='END',
 &end
EOF
	fi

	if [ ${HEAT} = "minimize" ]; then
cat > tmp.in << EOF
Initial minimization
&cntrl
ntx    = 1,       irest  = 0,       ntrx   = 1,      ntxo   = 1,
ntpr   = 20,      ntwx   = 0,       ntwv   = 0,      ntwe   = 0,

ntf    = 1,       ntb    = 1,
cut    = 9.0,     nsnb   = 10,

ibelly = 0,       ntr    = ${NTR},

imin   = 1,
maxcyc = 2000,
ncyc   = 100,
ntmin  = 1,       dx0    = 0.1,     dxm    = 0.5,     drms   = 0.0001,

ntc    = 1,       tol    = 0.00001,

&end
EOF
	fi


	if [ ${STEP} -le 27 ]; then
	  cat tmp.in restraints.txt > equil${STEP}.in
	else
	  cat tmp.in > equil${STEP}.in
	fi
done

