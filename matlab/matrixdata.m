d=[35.628 35.2 21.435]-[32.500  38.000  18.192]

mat=zeros([9 8])
x=1:9
mat(:,1)=x
793:4:826
mat(:,2)=ans
mat(1,3:5)=[36.530  18.864  21.435]

for i=1:9
mat(i,6:8)=mat(i,3:5)-d
end
dlmwrite ('test.dat', mat, ' ')