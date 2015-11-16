#!/bin/bash

# Initial seed
JID0=`qsub runObelix_mod3.sh`

I=1
while [ ${I} -le 10 ] ; do
  JIDN=`qsub -W depend=afterok:${JID0} runObelix_mod3.sh`
  JID0=${JIDN}
  sleep 5
  let "I+=1"
done
