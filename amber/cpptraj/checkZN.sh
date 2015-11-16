#! /bin/bash

# $1 -name of subdirectory
# $2 $3 - start and end of md*.nc files to use

i=$1
cd $i
rm -rf distZN
mkdir distZN
cd distZN

cat >ctraj.avg <<EOF
parm ../Cdp_UC${i%_rest}.prmtop
EOF

#for j in `ls -1rt ../RunEx/Trajectory/`
for j in `seq $2 $3`
do 
cat >>ctraj.avg <<EOF
trajin ../RunEx/Trajectory/md$j.nc
EOF
done

cat >>ctraj.avg <<EOF
average average.pdb pdb
distance :59@ZN :78@NE2  out A_HID@NE2.dat
distance :59@ZN :60@N    out A_SCN@N.dat 
distance :59@ZN :47@OE1  out A_GLU@OE1.dat
distance :59@ZN :58@OXT  out A_LYS@OXT.dat
distance :59@ZN :58@O    out A_LYS@O.dat
distance :59@ZN :47@OE2  out A_GLU@OE2.dat

distance :119@ZN :18@NE2  out B_HID@NE2.dat
distance :119@ZN :120@N    out B_SCN@N.dat 
distance :119@ZN :107@OE1  out B_GLU@OE1.dat
distance :119@ZN :118@OXT  out B_LYS@OXT.dat
distance :119@ZN :118@O    out B_LYS@O.dat
distance :119@ZN :107@OE2  out B_GLU@OE2.dat
EOF

cpptraj -i ctraj.avg >/dev/null
cat ../../../symheaderUC.txt average.pdb > ../../../vmd/Cdp.pdb

echo ${i}
cat >meanDist.py <<EOF
#! /usr/bin/python
from numpy import *
import sys
x=genfromtxt(sys.argv[1])
print "%10s %4.2f" %(sys.argv[1].split('.')[0], mean(x[:,1]))
EOF
chmod 775 meanDist.py
for i in `ls -1 A_*.dat`
do
./meanDist.py $i
done
echo -e "\n"
for i in `ls -1 B_*.dat`
do
./meanDist.py $i
done


cd ../../
