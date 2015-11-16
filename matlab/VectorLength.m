% VectorLength: compute the length of a vector by taking its dot product.
% The basis set in which the vector is expressed (often the unit cell
% parameters is input.
%
%   Arguments:
%   cellparameters: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%   v: a 1x3 array, the three components of the vector whose length I
%   want to find
%         
%   Usage:
%   vlen = VectorLength(cellparameters) returns the length of the matrix

function vlen  = VectorLength (cellparameters, v)
    a1=cellparameters(1);
    a2=cellparameters(2);
    a3=cellparameters(3);
    alpha=cellparameters(4);
    beta=cellparameters(5);
    gamma=cellparameters(6);
    
    vlen=(v(1)*a1)^2+(v(2)*a2)^2+(v(3)*a3)^2+2*v(1)*v(2)*a1*a2*cosd(gamma) ...
        +2*v(1)*v(3)*a1*a3*cosd(beta)++2*v(2)*v(3)*a2*a3*cosd(alpha);
end