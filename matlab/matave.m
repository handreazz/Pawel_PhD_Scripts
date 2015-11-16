for i = 0:1:35,
  fname = sprintf('Val/d%d.dat', i);
  tmp = load(fname);
  if (i == 1),
    dihe = zeros(size(tmp,1), 36);
  end
  dihe(:,i+1) = tmp(:,2);
end

rmsdihe = std(dihe')';
dihe = mean(dihe')';
npt = size(dihe,1)/200;
smdihe = zeros(npt,1);
for i = 1:1:npt,
  smdihe(i,1) = mean(dihe((i-1)*200+1:i*200,1));  
  smdihe(i,2) = mean(rmsdihe((i-1)*200+1:i*200,1));  
end
save ValDiheSmooth.dat smdihe -ascii
