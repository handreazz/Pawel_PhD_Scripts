% The goal of this script is to "mean center" the rows of matrix 
% (for every element x in column i, compute x - mean(A(:,i)) in two
% ways to emphasize the role of vectorization.

function [timeNoV, timeV, correct] = vectorization2(sizeMatrix)
    % 1. First try with no vectorization.
    A = randn(sizeMatrix);
    m = mean(A, 1);             % Take the mean over row vectors.
    B = zeros(sizeMatrix);      % Initialize the result matrix.
        
    tic;
    for i = 1:sizeMatrix
        for j = 1:sizeMatrix
            B(i,j) = A(i,j) - m(1, j);
        end
    end
    timeNoV = toc;
    
    % 2. Second try with vectorization
    tic;
    % Use repmat
    C = A - repmat(m, sizeMatrix, 1);
    timeV = toc;
    
    correct = (max(mean(B,1) - mean(C,1)) < 0.001);
end
