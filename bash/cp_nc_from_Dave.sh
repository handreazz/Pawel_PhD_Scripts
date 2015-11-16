#! /bin/bash
set -x
for i in 4 4.5 5 6; 
do
  cd $i
  cp /net/casegroup/u1/case/xtal/fav8/${i}/eq4-16.nc .
  cd ..
done


  
