%sampling frequency for Gaussiann
%is Gaussian also cyclic? What happens when I add two?
%reconstruct how?

mean=0;
sigma=.3;
dt=0.2;
%fs=1/dt;

x=-7:dt:7;
n=length(x);
%one gaussian
fx=1/sqrt(2*pi)/sigma*exp(-((x-mean).*(x-mean))/2/sigma/sigma);
%two gaussian
fx=1/sqrt(2*pi)/sigma*exp(-((x-mean+2).*(x-mean+2))/2/sigma/sigma)+1/sqrt(2*pi)/sigma*exp(-((x-mean-4).*(x-mean-4))/2/sigma/sigma);
figure(1)
plot(x,fx)


ft=fft(fx,n)/n;
ft0 = fftshift(ft);
%why divide by n?
t = (-n/2:n/2-1)*((1/dt)/n);
t = (-n/2:n/2-1)*((1/dt)/n);
y=abs(ft0);
figure(2)
plot(t,y), axis([-3 3 0 .2]);