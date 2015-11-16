% MetricTensor: compute the metric tensor  and reciprocal metric tensor 
%from the unit cell parameters
%
%   Arguments:
%   cellparameters: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%         
%   Usage:
%   gmet = MetricTensor(cellparameters) returns the (covariant) metric
%       tensor [This tensor converts reciprocal basis vectors to real
%       space(covariant) basis vectors. It also operates on real space vectors(contravariant components,
%       to produce reciprocal space vectors (covariant components).]
%   [gmet,gstar]=MetricTensor(cellparameters) returns the metric tensor and
%       the reciprocal(contravariant) metric tensor
%   [gmet,gstar,V]=returns the metric tensor, reciprocal metric tensor and
%   the volume of the real space unit cell

function [gmet, gstar,V]  = MetricTensor(cellparameters)
    gmet=zeros(3,3);
    for i=1:3; for j=1:3; if i==j;
    gmet(i,j)=cellparameters(i)*cellparameters(j);
            else
                if i+j==3
                    gmet(i,j)=cellparameters(i)*cellparameters(j)*cosd(cellparameters(6));
                elseif i+j==4
                    gmet(i,j)=cellparameters(i)*cellparameters(j)*cosd(cellparameters(5));
                elseif i+j==5
                    gmet(i,j)=cellparameters(i)*cellparameters(j)*cosd(cellparameters(4));

    end; end; end;end
    gstar=inv(gmet);
    V=sqrt(det(gmet));
end