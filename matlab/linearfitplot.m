function createFit(x)
data=load(x);
X=data(:,1);
Y=data(:,2);
plot(X,Y)
hold on
[pp,err]=fit(X,Y,'poly1')
plot(pp,'r-')
hold on
title('total diffusion tip3p water')
Ya=Y(1:500); %500 is the halfwaypoint, change to half of the number of frames in trajectory
Xa=X(1:500);
[ppa,erra]=fit(Xa,Ya,'poly1')
plot(ppa,'g-')
hold on
Xb=X(501:end);
Yb=Y(501:end);
[ppb,errb]=fit(Xb,Yb,'poly1')
plot(ppb,'g-')
xlabel('picosecons')
ylabel('A^{2}')