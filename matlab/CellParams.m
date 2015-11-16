% CellParams: compute cell parameters from a metric tensor
%
%   Arguments:
%   g: 3x3 metric tensor
%         
%   Usage:
%   cell = CellParams(g) 


function [cell]  = CellParams(g)
    cell=zeros(1,6);
    for i=1:3
        cell(i)=sqrt(g(i,i));
    end
    cell(4)=acosd(g(2,3)/(cell(2)*cell(3)));
    cell(5)=acosd(g(1,3)/(cell(1)*cell(3)));
    cell(6)=acosd(g(1,2)/(cell(1)*cell(2)));
end