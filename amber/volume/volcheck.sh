#!/bin/bash

./process_mdout.perl ../md1.out

cat > volcheck.m <<EOF

volume=cellvolume('../Eq0.rst7');
vol=load('summary.VOLUME');
MIN=min(vol(:,2))
MINPER=MIN/volume*100
MAX=max(vol(:,2))
MAXPER=MAX/volume*100
MEAN=mean(vol(:,2))
MEANPER=MEAN/volume*100
vol(:,2)=vol(:,2)./volume*100;
plot(vol(:,1),vol(:,2))
print myfile.jpg -djpeg
close(1)
pwd=pwd

fid=fopen('myvolume.txt','wt');
fprintf(fid, '%s\n',pwd);
fprintf(fid, 'crystal volume = %.2f\n', volume);
fprintf(fid, 'min volume = %.2f   %.2f percent\n', MIN, MINPER);
fprintf(fid, 'max volume = %.2f   %.2f percent\n', MAX, MAXPER);
fprintf(fid, 'mean volume = %.2f   %.2f percent\n', MEAN, MEANPER);
fclose(fid);
EOF

matlab -nosplash -nodisplay -nodesktop < volcheck.m > mtl.out

cat myvolume.txt
eog myfile.jpg &
