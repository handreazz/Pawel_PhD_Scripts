T = 1/1000;                     % Sample time
L = 1000;                     % Length of signal
t = (0:L-1)*T;                % Time vector
% Sum of a 50 Hz sinusoid and a 120 Hz sinusoid
x = 0.7*sin(2*pi*50*t) + sin(2*pi*120*t); 
y = x + 2*randn(size(t));     % Sinusoids plus noise

figure(1)
plot(t(1:50),y(1:50))
title('Signal Corrupted with Zero-Mean Random Noise')
xlabel('time (seconds)')


% FFT
% The scaling by L because fft in Matlab has no scaling, only ifft does.
% Since fft is summation of terms, the amplitude just keeps increasing with
% more grid points. So need to scale by L(the number of grid points).
% Alternatively, could scale fft and ifft by sqrt(L). 
Y = fft(y)/L;
f=(0:L-1)*(1/T)/L;

% Plot single-sided amplitude spectrum.
figure(2)
plot(f(1:L/2),2*abs(Y(1:L/2)));
title('Single-Sided Amplitude Spectrum of y(t)')
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')

