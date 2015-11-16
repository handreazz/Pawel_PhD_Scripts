#! /bin/bash

#make sure to edit sandbox.py
dir=../average_density/PDBData_nowat/
todo=`ls -1 $dir| wc -l`
done=0

for i in `ls -1 $dir`
do
  if [ $done -lt $todo ]; then
    echo $i
    ./getTrajContacts.py $dir/$i >residContact/${i%%.pdb}.dat
    let done=done+1
  fi
done


