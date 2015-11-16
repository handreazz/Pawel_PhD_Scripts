a=importdata('../Restart/md0.rst',' ',2);
ab=a.data(1:10224,:); %5184 is the number of atoms, change
b=importdata('../Restart/md1262.rst',' ',2);
bb=b.data(1:10224,:);


% Reshape the coordinate vectors from 2 atoms per line to 1 atom per line
firstframe = zeros(10224,3);
lastframe = zeros(10224,3);
for i = 1:1:5112,
  firstframe(2*(i-1)+1,:) = ab(i,1:3);
  firstframe(2*i,:) = ab(i,4:6);
  lastframe(2*(i-1)+1,:) = bb(i,1:3);
  lastframe(2*i,:) = bb(i,4:6);
end

SD=zeros(10224,3);
for i = 1:10224
for j = 1:3
SD(i,j)=(lastframe(i,j)-firstframe(i,j))^2;
end
end
xMSD=mean(SD(:,1))
yMSD=mean(SD(:,2))
zMSD=mean(SD(:,3))
totMSD=xMSD+yMSD+zMSD
DiffConst=totMSD/252400*10/6 %4000 is the time in picoseconds