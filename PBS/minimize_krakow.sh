#!/bin/bash


set -x

ROOT=$1

mpirun -np 4 pmemd.MPI -O \
  -i   minsolv.in \
  -o   minsolv.out \
  -c   ${ROOT}.rst7 \
  -p   ${ROOT}.prmtop \
  -ref ${ROOT}.rst7 \
  -r   ${ROOT}_minsolv.rst7

mpirun -np 4 pmemd.MPI -O \
  -i   minpro.in \
  -o   minpro.out \
  -c   ${ROOT}_minsolv.rst7 \
  -p   ${ROOT}.prmtop \
  -ref ${ROOT}_minsolv.rst7 \
  -r   ${ROOT}_minpro.rst7

mpirun -np 4 pmemd.MPI -O \
  -i   minall.in \
  -o   minall.out \
  -c   ${ROOT}_minpro.rst7 \
  -p   ${ROOT}.prmtop \
  -ref ${ROOT}_minpro.rst7 \
  -r   ${ROOT}_minall.rst7


