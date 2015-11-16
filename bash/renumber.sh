#!/bin/sh

for ((n=1; n<=9; n++))
do
   mv md${n}.out md000${n}.out
done

for ((n=10; n<=99; n++))
do
   mv md${n}.out md00${n}.out
done

for ((n=100; n<=999; n++))
do
   mv md${n}.out md0${n}.out
done

