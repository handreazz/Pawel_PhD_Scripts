#!/bin/bash
#
#PBS -N 2oueSg_ff10
#PBS -l nodes=1:ppn=4
#PBS -l walltime=72:00:00
#PBS -l cput=576:00:00
#PBS -l pvmem=2048mb
#PBS -o hpSfmin.out
#PBS -e hpSfmin.err
#PBS -V
#PBS -M pawelrc@gmail.com
#PBS -m bea

set -x
cd $PBS_O_WORKDIR

mpirun -np 4 pmemd.MPI -O -i minsolv.in -o minsolv.out -c 2oueSg_ff10.rst7 -p 2oueSg_ff10.prmtop -ref 2oueSg_ff10.rst7 -r 2oueSg_ff10.minsolv

mpirun -np 4 pmemd.MPI -O -i minpro.in -o minpro.out -c 2oueSg_ff10.minsolv -p 2oueSg_ff10.prmtop -ref 2oueSg_ff10.minsolv -r 2oueSg_ff10.minpro

mpirun -np 4 pmemd.MPI -O -i minall.in -o minall.out -c 2oueSg_ff10.minpro -p 2oueSg_ff10.prmtop -ref 2oueSg_ff10.minpro -r 2oueSg_ff10.minall
