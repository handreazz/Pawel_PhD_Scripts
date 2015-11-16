nrg = load('nrg.dat');
nrg = nrg(:,2);
sc = size(nrg,1);
vsm = zeros(sc/500,1);
for i = 1:1:sc/500,
  vsm(i,1) = mean(nrg((i-1)*500+1:i*500,1));  
end
save nrgSmooth.dat vsm -ascii
