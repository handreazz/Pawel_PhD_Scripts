function [ M ] = TLS_cross( A,B )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
M = sym('M',[3 3]);
for i=1:3;
    if size(B) == [1,3];
        M(i,1:3) = cross(A(i,1:3),B);
    elseif size(A) == [3,1];
        M(1:3,i) = cross(A,B(1:3,i));
    else;
        error('myApp:argChk', 'r wrong size')
    end     
end

end

