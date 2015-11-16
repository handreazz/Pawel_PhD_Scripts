A=load('A.txt');
b=load('B.txt');

size(A)
size(b)

x=llsp(A,b);
sA=size(A);
Aval=A(1:sA(1)-16,:);
bval=b(1:sA(1)-16);
t=corrcoef(Aval*x,bval);
fid=fopen('fitresult.txt','wt');
fprintf(fid, 'correlation = %12.8f\n', t(1,2));
fprintf(fid, 'rms error   = %12.8f\n\n', sqrt(sum((Aval*x-bval).^2)));
fprintf(fid, 'x = [\n');
fprintf(fid, '  %10.6f\n', x);
fprintf(fid, '];\n');
fclose(fid);
