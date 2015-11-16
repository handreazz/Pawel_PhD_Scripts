% Load data.  The data is to be loaded as massive column matrices where each
% matrix row represents one snapshot of the simulation, and each matrix column
% represents one of the 36 unit cells.  With a 40ps sampling rate, there should
% be 25 rows per ns of simulation, or 50,000 rows in all for a 2,000 ns run.
%t310 = load('Helicity310.dat');
%tVal = load('ValConf.dat');
%tH2O = load('WaterOcc.dat');

t310 = rand(50000,36);
tVal = rand(50000,36);
tH2O = rand(50000,36);

% Now, look for correlations among the rows of different matrices.  The number
% of timesteps nsteps is the length to which autocorrelation is calculated.
nsteps = 50;

% Count the number of frames in each analysis (better be equal)
if (sum(size(t310) - size(tVal)) ~= 0),
  fprintf('Error.  310 helicity and valine dihedral analyses cover different timescales.\n');
end
if (sum(size(t310) - size(tH2O)) ~= 0),
  fprintf('Error.  310 helicity and water occupancy analyses cover different timescales.\n');
end
ntrj = size(t310);
ntrj = ntrj(1,1);

c310vVal = zeros(nsteps, 1);
c310vH2O = zeros(nsteps, 1);
cValvH2O = zeros(nsteps, 1);

for i = 1:1:nsteps,

  % Average the correlation of all windows sampled over the whole trajectory.
  % The independence of consecutive windows is hardly guaranteed, and as the
  % window length grows the independence is sure to decrease.  But we can do
  % statistical inefficiency analysis in here as well, and taking all the
  % available windows gives us the maximum data since it's all averaged anyway.
  for j = 1:i:ntrj-(nsteps-1),
    
    % Compute the mean for this window
    if (i == 1),
      r310 = t310(j:j+i-1,:);
      rVal = tVal(j:j+i-1,:);
      rH2O = tH2O(j:j+i-1,:);
    else
      r310 = mean(t310(j:j+i-1,:));
      rVal = mean(tVal(j:j+i-1,:));
      rH2O = mean(tH2O(j:j+i-1,:));
    end

    % Compute correlations among the windows
    cc = corrcoef(r310, rVal);
    c310vVal(i,1) = c310vVal(i,1) + cc(1,2);
    cc = corrcoef(r310, rH2O);
    c310vH2O(i,1) = c310vH2O(i,1) + cc(1,2);
    cc = corrcoef(rVal, rH2O);
    cValvH2O(i,1) = cValvH2O(i,1) + cc(1,2);
  end
  c310vVal(i,1) = c310vVal(i,1) / floor(ntrj / i);
  c310vH2O(i,1) = c310vH2O(i,1) / floor(ntrj / i);
  cValvH2O(i,1) = cValvH2O(i,1) / floor(ntrj / i);

  fprintf('i = %d\n', i);
end
