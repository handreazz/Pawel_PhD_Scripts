#!/bin/bash

# Initial seed
JID0=`qsub runRangerEx3.sh`

I=1
while [ ${I} -le 2 ] ; do
  JIDN=`qsub -W depend=afterok:${JID0} runRangerEx3.sh`
  JID0=${JIDN}
  sleep 5
  let "I+=1"
done
