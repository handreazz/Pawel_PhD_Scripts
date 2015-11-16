vol = load('vol.dat');
vol = vol(:,2);
sc = size(vol,1);
vsm = zeros(sc/500,1);
for i = 1:1:sc/500,
  vsm(i,1) = mean(vol((i-1)*500+1:i*500,1));  
end
vsm = 100.0*(vsm-100645.15)/100645.15;
save volSmooth.dat vsm -ascii
