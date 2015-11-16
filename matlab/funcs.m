% The goal of the function is to emphasize several things:
% 1. Write a function.
% 2. Do some loops.
% 3. Memory preallocation.
% 4. Return the distribution over times for plotting.

function [timeNoP, timeP] = funcs(reps, sizeVector)
    timeNoP = zeros(reps, 1);
    timeP = zeros(reps, 1);
    
    for i = 1:reps
        % We make sure the two vectors are empty at the beginning.
        A = [];
        B = [];
        
        % First attempt with no preallocation.
        tic;        
        for j = 1:sizeVector
            A(j) = j;
        end
        timeNoP(i) = toc;
        
        % Second attempt with preallocation.        
        B = zeros(sizeVector, 1);
        tic;
        for j = 1:sizeVector
            B(j) = j;
        end
        timeP(i) = toc;
    end
end