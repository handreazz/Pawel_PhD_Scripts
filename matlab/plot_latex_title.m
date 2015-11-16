function createFit(x)
data=load(x);
X=data(:,1);
Y=data(:,2);
plot(X,Y)
hold on
[pp,err]=fit(X,Y,'poly1')
plot(pp,'r-')
hold on
%title('{\itAe}^{-\alpha\itt}sin\beta{\itt} \alpha<<\beta')
title('$$m \ddot y = -m g + C_D \cdot {1 \over 2}\rho {\dot y}^2 \cdot A$$','interpreter','latex')
% Ya=Y(1:(size(X)/2)+1);
% Xa=X(1:(size(X)/2)+1);
% [ppa,erra]=fit(Xa,Ya,'poly1')
% plot(ppa,'g-')
% hold on
% Xb=X((size(X)/2)+1:end);
% Yb=Y((size(X)/2)+1:end);
% [ppb,errb]=fit(Xb,Yb,'poly1')
% plot(ppb,'g-')
