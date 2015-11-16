#! /bin/bash

rm pressure.dat
touch pressure.dat

for i in `seq 7 48`; do
	grep "PRESS =" /casegroup/u1/case/xtal/4lzt_xtal/ff12SBi/md$i.o | awk '{print $NF }' |head -n -2 >tmp1.dat
	cat pressure.dat tmp1.dat >> tmp2.dat
	mv tmp2.dat pressure.dat
done
nl pressure.dat >tmp2.dat
mv tmp2.dat pressure.dat

rm tmp1.dat
