volume=cellvolume('../solvpep.rst7');

Etot=load('summary.ETOT');
Epot=load('summary.EPTOT');
Ekin=load('summary.EKTOT');
Pres=load('summary.PRES');
Vol=load('summary.VOLUME');
Temp=load('summary.TEMP');

hold()
plot(Etot(:,1),Etot(:,2), 'g')
plot(Epot(:,1),Epot(:,2), 'r')
plot(Ekin(:,1),Ekin(:,2), 'b')
legend('Etot', 'Epot', 'Ekin')
print Energy.jpg -djpeg
close(1)

plot(Pres(:,1),Pres(:,2))
legend('Pressure')
print Pressure.jpg -djpeg
close(1)

plot(Temp(:,1),Temp(:,2))
legend('Temperature')
print temperature.jpg -djpeg
close(1)



MIN=min(Vol(:,2))
MINPER=MIN/volume*100
MAX=max(Vol(:,2))
MAXPER=MAX/volume*100
MEAN=mean(Vol(:,2))
MEANPER=MEAN/volume*100
vol=Vol(:,2)./volume*100;
plot(Vol(:,1)/1e6,vol)
%legend('Volume as percentage of crystal volume')
xlabel('Time (ms)','FontSize',16)
ylabel('Volume (percent of crystal)','Fontsize',16)
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
