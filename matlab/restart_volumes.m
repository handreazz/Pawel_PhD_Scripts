V=zeros(41,2);
for i = 1:9
   i
   V(i,1)=i;
   file=sprintf('/home/case/xtal/fav8/amoeba/f%d.rst',i);
   V(i,2)=cellvolume(file); 
end

for i = 10:41
   i
   V(i,1)=i;
   file=sprintf('/home/case/xtal/fav8/amoeba/f%d.rst',i);
   V(i,2)=cellvolume(file); 
end