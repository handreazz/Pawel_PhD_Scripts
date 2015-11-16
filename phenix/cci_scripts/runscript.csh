#! /bin/csh -q
#$ -cwd
#$ -o queue.output -j y -N multi2 

limit datasize 2000000
#setup gcc-4.3.4_fc8_x86_64
source /net/cci-filer2/raid1/home/pawelrc/phenix_pawel2/build/setpaths_all.csh
phenix.refine diff.eff --quiet --overwrite
exit

