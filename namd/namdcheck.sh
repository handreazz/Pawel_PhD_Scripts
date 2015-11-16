#!/bin/bash

###need to change the location of the out files (first line below) and the location of the restart file with box dimensions(third line).

rm tmp.txt
OUTPUTS=../*log
#for i in `ls -ld ../${OUTPUTS} | grep ^- | awk '{print $9}' | grep ^${OUTPUTS}`; do
for i in `ls -d $OUTPUTS`; do
  grep ENERGY: $i >> tmp.txt
  done
cut -c9-320 tmp.txt >tmp2.txt

cat > volcheck.m <<EOF

volume=cellvolume('../equil30.rst7');
all=load('tmp2.txt');

plot(all(:,10))
print kineticE.jpg -djpeg
close(1)

plot(all(:,11))
print totalE.jpg -djpeg
close(1)

plot(all(:,11))
print totalE.jpg -djpeg
close(1)

plot(all(:,12))
print temp.jpg -djpeg
close(1)

plot(all(:,13))
print potentialE.jpg -djpeg
close(1)

plot(all(:,15))
print tempAvg.jpg -djpeg
close(1)

plot(all(:,16))
print pressure.jpg -djpeg
close(1)

plot(all(:,19))
print pressureAvg.jpg -djpeg
close(1)

MIN=min(all(:,18))
MINPER=MIN/volume*100
MAX=max(all(:,18))
MAXPER=MAX/volume*100
MEAN=mean(all(:,18))
MEANPER=MEAN/volume*100
vol=all(:,18)./volume*100;
plot(vol)
print volume.jpg -djpeg
close(1)
pwd=pwd

fid=fopen('volume.txt','wt');
fprintf(fid, '%s\n',pwd);
fprintf(fid, 'crystal volume = %.2f\n', volume);
fprintf(fid, 'min volume = %.2f   %.2f percent\n', MIN, MINPER);
fprintf(fid, 'max volume = %.2f   %.2f percent\n', MAX, MAXPER);
fprintf(fid, 'mean volume = %.2f   %.2f percent\n', MEAN, MEANPER);
fclose(fid);
EOF

matlab -nosplash -nodisplay -nodesktop < volcheck.m > mtl.out

cat volume.txt
eog volume.jpg &
