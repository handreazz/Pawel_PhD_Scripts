volume=cellvolume('XtalxN.crd');
vol=load('summary.VOLUME');
vol(:,2)=vol(:,2)./volume*100;
plot(vol(:,1),vol(:,2))
print myfile.jpg -djpeg
close(1)