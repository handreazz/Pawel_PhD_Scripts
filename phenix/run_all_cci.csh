#! /bin/csh -q
#$ -cwd
#$ -o queue.output -j y -N amber
limit datasize 2000000

source /net/chevy/raid1/nigel/phenix_amber_build/setpaths.csh

elbow.python run_tests.py  only_i=$SGE_TASK_ID >& output/job.$SGE_TASK_ID.output

exit
