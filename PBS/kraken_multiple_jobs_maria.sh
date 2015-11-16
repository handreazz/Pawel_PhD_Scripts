!/bin/bash

#PBS -A TG-CHE100072
#PBS -l size=216,walltime=24:00:00
#PBS -q small

nCPU=216
START_FRAME=1
END_FRAME=100

export MPICH_PTL_SEND_CREDITS=-1
export MPICH_MAX_SHORT_MSG_SIZE=8000
export MPICH_PTL_UNEX_EVENTS=80000
export MPICH_UNEX_BUFFER_SIZE=100M

pmemd=/nics/a/proj/CHE100072/amber040411/bin/pmemd.MPI

jobListFile="$HOME/Jobs"
tempListFile=$jobListFile.$PBS_JOBID
/bin/cp $jobListFile $tempListFile
jobList=`cat $tempListFile`

nJob=`cat $jobListFile | wc -l`

let nCPUPerJob=$nCPU/$nJob
#nCPUPerJob=12

echo "XXX" $nJob $nCPU $nCPUPerJob

#i=1

for ((i=$START_FRAME; i<=$END_FRAME; i+=1)); do
    let j=$i+1
    for job in $jobList
    do
      echo $i $job
      cd $job
      aprun -n $nCPUPerJob $pmemd -O -i Mg_md.in -o Mg1_mod_md$j.out -p Mg1_mod.parm7 -c Mg1_mod_md$i.rst -r Mg1_mod_md$j.rst -x Mg1_mod_md$j.crd &
    done
    #let "i = $i+1"
    wait
done


