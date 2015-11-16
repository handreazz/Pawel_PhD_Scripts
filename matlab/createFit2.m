% Creates plot of diffusion output from ptraj. Fits line (red) to entire
% plot and green to first half and second half of plot to give error
% estimates.

%arguments
%   half: half of the number of frames in the trajectory


function createFit(x)
%half=12000
%tit='x axis diffusion'


data=load(x);
x1=data(1:22500,:);
x2=data(25000:end,:);

[pp1,err1]=fit(x1(:,1),x1(:,2),'poly1')
[pp2,err2]=fit(x2(:,1),x2(:,2),'poly1')

l1x=1:100:500000;
l1y=l1x*pp1.p1+pp1.p2;

l2x=500000:100:2400000;
l2y=l2x*pp2.p1+pp2.p2;

plot(data(:,1),data(:,2))
hold on
plot(l1x,l1y,'r-')
plot(l2x,l2y,'r-')

%title(tit)
%~ Ya=Y(100:half);
%~ Xa=X(100:half);
%~ [ppa,erra]=fit(Xa,Ya,'poly1')
%~ plot(ppa,'g-')
%~ hold on
%~ Xb=X(half:end);
%~ Yb=Y(half:end);
%~ [ppb,errb]=fit(Xb,Yb,'poly1')
%~ plot(ppb,'g-')
