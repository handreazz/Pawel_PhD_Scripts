%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Creation of matrices %
%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Simple creation of a vector - create a row vector (the default type in
% matlab)
v1 = [1 2 3]

% Equivalently, we can use commas.
v2 = [1, 2, 3]

% To create a column vector we can either transpose a row vector 
% by using the transpose operator '
c1 = [1 2 3]'

c2 = v2'

% Or use a semicolon between the vector components.
c3 = [1; 2; 3]

% Matrices are created similarly - as a sequence of rows
m1 = [1 2 ; 3 4]

% Or as a sequence of columns
m2 = [4 5 ; 6 7]'

% Useful functions for automatic generation of vectors / matrices.
m = zeros(10)       % 10x10 matrix filled with zeros.
v = zeros(1,10)     % row vector with 10 elements filled with zeros.

m = ones(2)         % 2x2 matrix filled with ones
m = randn(3)        % 3x3 matrix of numbers ~ Normal(0,1)
m = eye(3)          % 3x3 identity matrix

% Other shortcuts - use ':'
v = [1:10]          % vector with elements 1..10
v = [1:2:10]        % 1 to 10, every 2 numbers.

% To find the size of a matrix:
size(m)

% To find the number of rows:
size(m, 1)

%%%%%%%%%%%%%%%%%%%%%%%
% 2. Basic operations %
%%%%%%%%%%%%%%%%%%%%%%%
% Operations on rows or columns
m = rand(3)
sum(m, 1)           % sums the rows
sum(m, 2)           % sums the columns
mean(m, 1)          % takes the means among rows

% Concatenation
b = [m m]           % creates a 3x6 matrix by repeating m two times
% Or a more elegant way - use the repmat function to "repeat" m 
% for an 1x2 blocks of 3x3 submatrices.
b = repmat(m, 1, 2) 

%%%%%%%%%%%%%%%
% 3. Indexing %
%%%%%%%%%%%%%%%
m = [1 2 3; 4 5 6]
x = m(1,2)          % element in row 1 column 2
x = m(:,3)          % 3rd column
x = m(2, :)         % 2nd row
x = m(:)            % 

% Get the element on the left of the bottom right corner of m.
x = m(end, end - 1)

% Get the main diagonal of m
x = diag(m)

% Linear indexing - set the elements of the matrix in order from 1
% to the size of the matrix. Linear indexing goes top to bottom and 
% then left to right.
m = zeros(3,4)
m(1:numel(m)) = 1:numel(m)  % Creates a matrix with elements from 1 to 12.

% Logical indexing.
m = [1 2 3 ; 4 5 6]
a = m > 5           % Returns a 'logical' matrix with 0 = false, 1 = true

% Returns a vector of all the elements satisfying the logical expression.
a = m((m>2) & (m<5))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% 4. Element-wise operations %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
m = zeros(3)
m = m + 1           % Adds 1 to every element.
m = m .* 2          % Multiply every element with 2.

n = zeros(3)
n(1:9) = 1:9

r = m.*n            % Multiply the matrices element by element.
r = m.^n            % Raise the elements of m to the powers from n.

%%%%%%%%%%%%%%%%%%%%%
% 5. Multiplication %
%%%%%%%%%%%%%%%%%%%%%
r = m * n           % Regular matrix multiplication.
r = m^3             % m*m*m

%%%%%%%%%%%%%%%%%%%%%
% 6. Linear systems %
%%%%%%%%%%%%%%%%%%%%%
A = randn(10, 3)
x = randn(3, 1)
b = A * x

% If x is unknown, we find it by using the division operator \.
x1 = A \ b          % In this case the solution is indeed x.
x1 == x             % Check that they are equal

% A bit of profiling
tic                 % Start a timer
% do some stuff
toc                 % End the timer and get the results in seconds.

% Let's try a different way of finding x if unknown. We apply the
% standard least squares solution: x = inv(A'*A)*A'*b and profile it. 
% To make profiling interesting we create larger matrices.
A = randn(1000, 1000);
x = randn(1000, 1);
b = A * x;

% First version.
tic
x1 = A\b;
t1 = toc;

% Second version.
tic;
x2 = inv(A'*A)*A'*b;
t2 = toc;

% Find how much faster was the first option.
t2 / t1