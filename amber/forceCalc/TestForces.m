LoadHairpin;
path(path,'/home/cerutti/EwaldTest/src/MatlabEwald');

%This will test my settings of PME calculation.
Lcut = 10
ordr = [4 4 4]
Dtol = 1e-05
ng = [96 96 132]
%[frc,fdir,frec] = pmeMain(crdq, ng, gdim, ordr, Dtol, Lcut);

%This will be a reference calculation
Lcut = 12.461238149;
ordr = [6 6 6]
Dtol = 1e-07
ng = [192 192 256]
[frcR2,fdirR2,frecR2] = pmeMain(crdq, ng, gdim, ordr, Dtol, Lcut);

%This will test new, 6th order settings of PME calculation.
Lcut = 10
ordr = [6 6 6]
Dtol = 1e-05
ng = [64 64 90]
%[frcE,fdirE,frecE] = pmeMain(crdq, ng, gdim, ordr, Dtol, Lcut);