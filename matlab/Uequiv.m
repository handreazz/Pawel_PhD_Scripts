%This will calculate the Uequiv from the Uani's in a cif file.
%Must have the variables gdim (vector of 

%   Arguments:
%   gdim: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%         (actually you don't need the angles, just the three lattice
%         vector lenghts)
%   stdim: a 1 x 6 array, the lengths of the reciprocal lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%         (actually you don't need the angles, just the three lattice
%         vector lenghts)
%   ani: the 1x6 array containing the 6 unique elements of the Uani tensor
%        in cif order ani=(U11 U22 U33 U23 U13 U12)
%   method: 1 (count each of the six different Uani once) or 2 (count the off diagnonal elements of the 
%            Uani twice) 3: this is the one that works! Method 1 and 2 are
%            wrong.
%
%   Usage:
%   Ueq=Uequiv(gdim, stdim, ani, method) returns the isotropic Uequiv
%   [Ueq, Bfac] = Uequiv(gdim, stdim, ani, method) returns both the
%   isotropic Uequiv and the isotropic B-factor


function [Ueq, Bfac]  = Uequiv(gdim, stdim, ani, method)
Ueq=0;

if method==1;
    for i=1:3; for j=1:3;
     if i<=j;
        if i==j
           Ueq=Ueq + ani(i)*stdim(i)*stdim(j)*gdim(i)*gdim(j);
        elseif i+j==3
            Ueq=Ueq + (ani(6)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
        elseif i+j==4
            Ueq=Ueq + (ani(5)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
        elseif i+j==5
            Ueq=Ueq + (ani(4)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
     end;end;end;end
end
 
if method==2;
    for i=1:3; for j=1:3;
     if i<=j;
        if i==j
           Ueq=Ueq + ani(i)*stdim(i)*stdim(j)*gdim(i)*gdim(j);
        elseif i+j==3
            Ueq=Ueq + 2*(ani(6)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
        elseif i+j==4
            Ueq=Ueq + 2*(ani(5)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
        elseif i+j==5
            Ueq=Ueq + 2*(ani(4)*stdim(i)*stdim(j)*gdim(i)*gdim(j));
     end;end;end;end
end

if method==3;
    Ueq=ani(1)*gdim(1)*stdim(1)*gdim(1)*stdim(1)...
        +ani(2)*gdim(2)*stdim(2)*gdim(2)*stdim(2)...
        +ani(3)*gdim(3)*stdim(3)*gdim(3)*stdim(3)...
        +2*ani(6)*gdim(1)*gdim(2)*stdim(1)*stdim(2)*cosd(gdim(6))...
        +2*ani(5)*gdim(1)*gdim(3)*stdim(1)*stdim(3)*cosd(gdim(5))...
        +2*ani(4)*gdim(2)*gdim(3)*stdim(2)*stdim(3)*cosd(gdim(4));
end    

Ueq=Ueq/3;
Bfac=Ueq*8*pi^2;

end