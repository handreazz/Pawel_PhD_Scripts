% Load data
ndihe = 576;
tmp = load('Val/d1.dat');
sc = size(tmp);
nfrm = sc(1,1);

TD = zeros(nfrm,ndihe);
for i = 1:1:ndihe,
  fname = sprintf('Val/d%d.dat', i);
  tmp = load(fname);
  TD(:,i) = tmp(:,2);
end

% Take care of 180-degree dihedrals
for i = 1:1:ndihe,
  stdimgsum = abs(sum(TD(2:nfrm,i) - TD(1:nfrm-1,i)));
  newimg = TD(:,i) + 180.0;
  for j = 1:1:nfrm,
    if (newimg(j,1) > 180.0),
      newimg(j,1) = newimg(j,1) - 360.0;
    end
  end
  newimgsum = abs(sum(newimg(2:nfrm,1) - newimg(1:nfrm-1,1)));
  if (newimgsum < stdimgsum),
    TD(:,i) = newimg;
  end
end
  
% Smooth the dihedral trajectory
nsmooth = 100;
TDs = zeros(nfrm/nsmooth, ndihe);
for i = 1:1:ndihe,
  TDs(i,:) = mean(TD((i-1)*nsmooth+1:i*nsmooth,:));
end

% Compute correlation matrix
CorrMat = ones(ndihe, ndihe);
for i = 1:1:ndihe-1,
  for j = i+1:1:ndihe,
     g = corrcoef(TDs(:,i), TDs(:,j));
     CorrMat(i,j) = g(1,2);
     CorrMat(j,i) = g(2,1);
  end
end

% Group all 16 angles
nasu = ndihe / 16;
for i = 1:1:nasu,
  for j = 1:1:16,
    DiheGrp(:,i,j) = TDs(:,(i-1)*16+j);
  end
end

