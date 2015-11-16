% DotProduct: compute the dot product of two vectors.
%
%   Arguments:
%   cellparameters: a 1 x 6 array, the lengths of the lattice vectors in Angstroms
%         followed by the box Alpha, Beta, and Gamma angles in degrees
%   v,u: two 1x3 arrays representing the two vectors of which I want to
%   find the dot product
%         
%   Usage:
%   uv = DotProduct(cellparameters,u,v) returns the dot product of the two
%   vectors, if u=u

function uv  = DotProduct (cellparameters, u, v)
    a1=cellparameters(1);
    a2=cellparameters(2);
    a3=cellparameters(3);
    alpha=cellparameters(4);
    beta=cellparameters(5);
    gamma=cellparameters(6);
    
    uv=0;
    g=MetricTensor(cellparameters);
    for i=1:3
        for j=1:3
            uv=uv+u(i)*v(j)*g(i,j);
        end
    end
end