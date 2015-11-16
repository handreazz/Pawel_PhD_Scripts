
% Example of running optimization on 3sets of data modelled with 3 separate
% equations but common parameters. Here I use lsqnonlin to do this. This
% matlab function requires handle to the error function (not the sum of
% squared errors!). Could also have used lsqcurvefit which requires X,Y
% data (instead of error function) or fminunc (which requires the sum of
% squared errors and minimizes that function directly). There's also nlinfit.
% See also: 
% http://www.mathworks.com/help/optim/examples/nonlinear-data-fitting.html



%============================%
%                            %
% GENERATE SYNTHETIC DATA    %
%                            %
%============================%

%3 equations
f=@(A,B,x)A*x.^2+B*x;
g=@(A,B,x)A*x.^3+B*x;
h=@(A,B,x)A*x.^3+B*x.^2;

%x-values and parameters
x=[-5:1:5];
A=2;
B=7;

%y-values
y1=f(A,B,x)+rand(1,size(x,2));
y2=g(A,B,x)+rand(1,size(x,2));
y3=h(A,B,x)+rand(1,size(x,2));

%Final Data matrix with boolean columns
X=zeros(33,5);
X(:,1)=[x,x,x];
X(1:11,2)=1;
X(12:22,3)=1;
X(23:33,4)=1;
X(:,5)=[y1,y2,y3];


%========================================%
%                                        %
% FIT CURVES TO FIND BEST LSQ PARAMETERS %
%                                        %
%========================================%

%guess initial parameters
n=[1,1]

%optimize: ErrorFunction is called from separate file. The first argument
%to error function must contain all the arguments to be optimized. Then
%three empty matrices are supplied for the lbn, ubn, and options. Finally
%supply remaining parameters to Error Function that are given (not
%optimized).
lsqnonlin(@ErrorFun,n,[],[],[],X)

% Also works in this case
% E=@(n,X)X(:,2).*(eq1(n(1),n(2),X(:,1))-X(:,5)) + X(:,3).*(eq2(n(1),n(2),X(:,1))-X(:,5)) + X(:,4).*(eq3(n(1),n(2),X(:,1))-X(:,5));
% lsqnonlin(E,[1,2],[],[],[],X)

