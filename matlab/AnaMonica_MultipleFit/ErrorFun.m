function E = ErrorFun(Params,Data)

A=Params(1);
B=Params(2);
X=Data;

%Generate Data
eq1=@(A,B,x)A*x.^2+B*x;
eq2=@(A,B,x)A*x.^3+B*x;
eq3=@(A,B,x)A*x.^3+B*x.^2;

E=X(:,2).*(eq1(A,B,X(:,1))-X(:,5)) + X(:,3).*(eq2(A,B,X(:,1))-X(:,5)) + X(:,4).*(eq3(A,B,X(:,1))-X(:,5));



