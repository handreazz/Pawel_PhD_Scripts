figure(1)
%n = [0:29]*.1;
%specify period and sampling frequency. By nyquist, the sampling must be at
%least half of the highest frequency component (1/period/2)
period=1.5
sampl_freq=.6
n = [0:6/sampl_freq]*sampl_freq;
dt=n(2);
x = cos(2*pi*n/period);
plot(n,x)

% Nyquist freq is obtained with 20 in this case? Why if that means I'm
% sampling every 3/20=0.15s but the period is 1s?
N1 = size(n,2);
N2 = 128;
N3 = 256;
X1 = abs(fft(x,N1));
X2 = abs(fft(x,N2));
X3 = abs(fft(x,N3));

% To get correct x-axis units, multiply by inverse of time units. Buy I
% also need to divide by N. Why?
F1 = [0 : N1 - 1]/N1*(1/dt);
F2 = [0 : N2 - 1]/N2*(1/dt);
F3 = [0 : N3 - 1]/N3*(1/dt);

figure(2)
subplot(3,1,1)
plot(F1,X1,'-x'),title('N = 64'),axis([0 10 0 20])
subplot(3,1,2)
plot(F2,X2,'-x'),title('N = 128'),axis([0 10 0 20])
subplot(3,1,3)
plot(F3,X3,'-x'),title('N = 256'),axis([0 10 0 20])