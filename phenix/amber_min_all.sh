#! /bin/bash

#~ for stru in 1ad0 1BZQ 1exr  ; do

for stru in 1ad0  ; do
  
  cd 1ad0
  phenix.amber_geometry_minimization \
    4phenix_$stru.pdb \
    amber.use=True \
    amber.topology_file_name=$stru.prmtop \
    amber.coordinate_file_name=$stru.rst7 \
    output=ambermin
  phenix.amber_geometry_minimization \
    4phenix_$stru.pdb \
    amber.use=False \
    amber.topology_file_name=$stru.prmtop \
    amber.coordinate_file_name=$stru.rst7 \
    output=phenixmin
  phenix.molprobity ambermin.pdb
  mv molprobity.out ambermin_molprobe.out
  phenix.molprobity phenixmin.pdb  
  mv molprobity.out phenixmin_molprobe.out
  
  cat >> ../amber_min_summary.txt <<EOF


$stru  
amber  
EOF
  tail ambermin_molprobe.out >> ../amber_min_summary.txt
  cat >> ../amber_min_summary.txt <<EOF
phenix
EOF
  tail phenixmin_molprobe.out >> ../amber_min_summary.txt
  
  cd ..

done
