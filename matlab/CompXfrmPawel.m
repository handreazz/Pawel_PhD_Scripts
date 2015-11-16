% CompXfrm: compute transformation matrices for taking coordinates into
%           and out of box space for a unit cell of dimensions gdim.  Note
%           that gdim is assumed to be a 1 x 6 vector; no checking for its
%           size is done here.
%
%   Arguments:
%   gdim: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in radians
%         (if these angles are not supplied, they will be assumed to be
%         pi/2)
%
%   Usage:
%   [U] = CompXfrmPawel(gdim) returns the transformation matrix for taking
%     coordinates or displacement vectors from cartesian coordinates 
%     into box space (fractional coordinates) (inverse of the
%     orthogonalization matrix). To do this for a vector v: U*transpose(v).
%   [U,invU] = CompXfrmPawel(...) returns the transformation matrix as well as
%     its inverse, invU is the matrix to transform fractional coordiantes into
%     cartesian coordinates (real space coordinates) (orthogonalization matrix)
%   [U,invU, V] = CompXfrmPawel(...) returns the transformation matrix, the
%   inverse and the unit cell volume.
%
%   ###To change cartesian coordinates into fractional. If the vector in
%   cartesian coordinates is r=[x y z], you must do u*r'. Ie you must
%   operate the matrix on the vector and the vector must be vertical for
%   the mutliplication to work!!!

function [U,invU,V] = CompXfrm(gdim)

  szg = size(gdim);
  szg = szg(2);
  if (szg == 3),
    gdim(4:6) = 0.5*pi;
  end

  a=gdim(1);
  b=gdim(2);
  c=gdim(3);
  alpha=gdim(4);
  beta=gdim(5);
  gamma=gdim(6);

  V=a*b*c*sqrt(1-cos(alpha)^2-cos(beta)^2-cos(gamma)^2+2*cos(alpha)*cos(beta)*cos(gamma));
  
  invU = zeros(3,3);
  invU(1,1) = a;
  invU(1,2) = b*cos(gamma);
  invU(1,3) = c*cos(beta);
  invU(2,2) = b*sin(gamma);
  invU(2,3) = c*(cos(alpha)-(cos(beta)*cos(gamma)))/sin(gamma);
  invU(3,3) = V/(a*b*sin(gamma));
  U = inv(invU);
end
