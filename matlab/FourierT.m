mean=2;
sigma=.25;
dt=0.1;
fs=1/dt;

x=-3:dt:3;
n=length(x);
fx=1/sqrt(2*pi)/sigma*exp(-(x.*x)/2/sigma/sigma);
figure(1)
%plot(x,fx)

figure(2)
ft=fft(fx);
ft0 = fftshift(ft);
t = (-n/2:n/2-1)*(fs/n);
y=abs(ft0);
%plot(t,y)