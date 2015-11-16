% Recip: compute reciprocal cell parameters
%
%   Arguments:
%   gdim: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%         
%   Usage:
%   stdim = Recip(gdim) returns the reciprocal cell parameters (angles in degrees of the unit
%   cell with real space parameters gdim


function stdim  = Recip (gdim)
%gdim(4:6)=gdim(4:6)*pi/180
[gmet,gstar]=MetricTensor(gdim);
stdim=zeros(1,6);

stdim(1)=sqrt(DotProduct(gdim,gstar(1:3,1),gstar(1:3,1)));
stdim(2)=sqrt(DotProduct(gdim,gstar(1:3,2),gstar(1:3,2)));
stdim(3)=sqrt(DotProduct(gdim,gstar(1:3,3),gstar(1:3,3)));

stdim(4)=acosd((DotProduct(gdim,gstar(1:3,2),gstar(1:3,3)))/(stdim(2)*stdim(3)));
stdim(5)=acosd((DotProduct(gdim,gstar(1:3,1),gstar(1:3,3)))/(stdim(1)*stdim(3)));
stdim(6)=acosd((DotProduct(gdim,gstar(1:3,1),gstar(1:3,2)))/(stdim(1)*stdim(2)));
end